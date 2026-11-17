# CLI registry — detection, auth signals, and tier-3 probes

What `scripts/scan.sh` checks per CLI (tiers 1–2, zero tokens) and the exact live probe
the agent runs for tier 3. One probe attempt per model; a probe you did not run leaves
the status `unverified`.

## Probe classification (applies to every CLI)

Run the probe once with a 120s timeout. Classify by what you observed:

| Observation | Model status | Evidence to record |
|---|---|---|
| exit 0 and output contains `ok` | `verified` | probe command + "replied ok" |
| error naming the model, plan, or permission ("model not found", "invalid model", "not included in your plan", 403) | `unavailable` | first error line, quoted |
| login/credential error ("not logged in", "unauthorized", 401, "invalid API key", "authentication") | set the CLI's `auth.status` to `unauthenticated`; every model → `blocked-by-auth` | first error line, quoted |
| quota/rate-limit error ("quota exhausted", 429, "rate limit") | `quota-exhausted` — the account IS active; exclude from routing this scan, quote the reset time if given | first error line, quoted |
| usage/flag error | retry once after fixing the flag from `<cli> --help`; second failure → `unknown` | the usage error, quoted |
| timeout or network error | `unknown` — never `unavailable` | "probe timed out after 120s" |

A probe costs a few tokens (well under $0.01/model). Never loop or bulk-retry probes.
Classify from the **output text**, not the exit code alone — some CLIs exit 0 while printing
an error, and a probe piped through `tail`/`head` reports the pipe's exit, not the CLI's.

**Resolving what `default` actually is** — two sources, record both when you have them:

1. Config read (scan.sh does this, zero tokens): the `default_model` field on the CLI entry,
   from the config paths listed per CLI below. Absent key = the CLI's built-in default, which
   is not readable locally — the field honestly says `unknown`.
2. Probe banner (ground truth): when the probe output prints the resolved model — opencode's
   `<agent> · <model>` header, codex's `model: ...` session line — record it as `resolved_id`
   on the `default` model entry. Banner beats config: it's what actually ran. No banner and no
   config → leave `resolved_id` off; never guess a model id from memory of the CLI's docs.

## claude (Claude Code)

- **Invocation for consumers:** `agent-tool` — sub-agents spawned via the Agent tool ride the current session's auth; probes here verify the *plan* (e.g. is fable included), not connectivity.
- **Auth heuristics (scan.sh):** env `ANTHROPIC_API_KEY` → `~/.claude/.credentials.json` (Windows/Linux) → `oauthAccount` in `~/.claude.json` (covers macOS Keychain storage).
- **Seed models:** the stable tier aliases `haiku sonnet opus fable` — never dated model ids; aliases resolve at spawn time and don't rot.
- **Probe:** `claude -p "Reply with exactly: ok" --model <alias>`

## codex (OpenAI Codex CLI)

- **Auth heuristics:** `codex login status` output → `~/.codex/auth.json` → env `OPENAI_API_KEY`.
- **Default model:** `model =` in `~/.codex/config.toml`; probe banner prints a `model: ...` session line.
- **Seed models:** `default` only — bash workers just need "the CLI works"; add explicit `-m <id>` probes only if the user asks for a specific model.
- **Probe:** `codex exec --skip-git-repo-check "Reply with exactly: ok"`

## gemini (Gemini CLI)

- **Auth heuristics:** env `GEMINI_API_KEY` → env `GOOGLE_API_KEY` → `~/.gemini/oauth_creds.json`.
- **Default model:** `"model"` key in `~/.gemini/settings.json`; note gemini silently falls back pro→flash under quota pressure, so config ≠ guaranteed.
- **Seed models:** `default`.
- **Probe:** `gemini -p "Reply with exactly: ok"` (specific model: add `-m <id>`)

## copilot (GitHub Copilot CLI)

- **Auth heuristics:** `~/.copilot` config dir presence only — always `unknown` until probed.
- **Default model:** `"model"` key in `~/.copilot/config.json`.
- **Seed models:** `default`.
- **Probe:** `copilot -p "Reply with exactly: ok"` — flag surface changes between releases; on a usage error, check `copilot --help` and retry once.

## opencode

- **Auth heuristics:** `~/.local/share/opencode/auth.json`.
- **Default model:** `"model"` key in `~/.config/opencode/opencode.json` (a project-local `opencode.json` can override it — the scan reads the global one); probe banner prints `<agent> · <model>`.
- **Seed models:** `default`.
- **Probe:** `opencode run "Reply with exactly: ok"`

## qwen (Qwen Code)

- **Auth heuristics:** `~/.qwen/oauth_creds.json` → env `DASHSCOPE_API_KEY` → env `QWEN_API_KEY`.
- **Default model:** `"model"` key in `~/.qwen/settings.json`.
- **Seed models:** `default`.
- **Probe:** `qwen -p "Reply with exactly: ok"` (gemini-cli fork, same flag surface; specific model: add `-m <id>`)

## ollama (local models)

- **No account, no probe:** `ollama list` is ground truth — every listed model is `verified` at scan time, for free. `ollama list` failing with the binary present means the server isn't running (auth `unknown`, not `unauthenticated`).
- **Invocation:** `bash` (`ollama run <model> "<prompt>"`).

## Adding a CLI

1. In `scan.sh`: add an `auth_<name>()` heuristic (check files/env *names*, never print values) and a `scan_cli <name> auth_<name> "<seeds>" bash` line.
2. Add a section here: auth signals, seed models, probe command.
3. Rerun the skill — the new CLI flows into the inventory and (if its default probe verifies) into `routing.bash_workers`.
