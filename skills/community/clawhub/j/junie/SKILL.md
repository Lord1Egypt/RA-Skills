---
name: junie
description: Install, update, authenticate, configure, and direct JetBrains Junie CLI in Junie-native ways on macOS or Linux shells. Use when a host agent should steer Junie iteratively toward an overall goal, especially when the host agent has broader context than Junie, Junie should carry out focused implementation/review work, or the task may benefit from Junie-accessible models not available to the host agent. Also use when asked to set up Junie, verify an existing install, create or adjust ~/.junie/config.json or project .junie/config.json, bootstrap a repo’s .junie layout, wire in skills/guidelines/MCP/model locations, prepare Junie for CI headless usage, or decide whether interactive Junie flows truly require headless-terminal-style PTY control. Trigger on limited host-agent command phrases such as /junie help, /junie status, /junie model, /junie usage, /junie bootstrap, and /junie dry-run.
---

# Junie

Use this skill to set up Junie CLI without guessing and without fighting Junie’s own conventions. Also use it when the host agent should act as the planner/reviewer while Junie acts as a focused implementation or review agent. Prefer Junie’s documented non-interactive surfaces first: installer script, CLI flags, environment variables, and `config.json`. Preserve Junie’s standard `.junie/` layout unless the user explicitly wants something custom. Reach for interactive TUI driving only when the task genuinely requires the welcome screen or `/account` flow.

## Junie ecosystem guardrails

- Prefer project-shared configuration in `<project>/.junie/`.
- Prefer personal defaults in `~/.junie/`.
- Prefer `.junie/AGENTS.md` for reusable project guidance instead of inventing a custom location.
- Prefer `.junie/skills/`, `.junie/commands/`, `.junie/agents/`, `.junie/models/`, `.junie/mcp/`, and `.junie/rules/` when bootstrapping a repo.
- Treat `~/.junie/settings.json` as Junie-owned runtime state; do not edit it unless the user explicitly asks.
- Ask before persisting secrets to durable config. Environment variables are usually better for CI and temporary setup.

## Primary use cases

Use Junie as an iterative execution partner when the host agent should direct a body of work but Junie should carry out focused repo-local steps. In this mode:
- The host agent owns the overall goal, context synthesis, task shaping, risk management, and acceptance checks.
- Junie owns the focused implementation, review, or repo operation it has been briefed to perform.
- Expect some back and forth: the host agent briefs Junie, inspects the result, then either accepts it, asks a targeted follow-up, or corrects small issues directly.
- Prefer this mode when the host agent has more relevant context than Junie, especially prior discussion, cross-system evidence, user preferences, project doctrine, or sensitive constraints that Junie would not infer from the repo alone.
- Consider this mode when Junie can use models or model/tool combinations that the host agent cannot access directly.

When model choice matters, recommend the best fit for the task, but treat the user as the final authority. Stronger Junie models may imply heavy quota or billing utilization, so do not silently choose an expensive model for a substantial run unless the user has already approved that posture.

## Workflow

1. Inspect the current state.
2. Install or update Junie if needed.
3. Choose an authentication path.
4. Decide whether this is setup/config work or iterative Junie-directed execution.
5. Write or merge configuration conservatively.
6. Brief Junie sharply when using it as an execution partner.
7. Verify with the smallest meaningful check.
8. Use `headless-terminal` only if the interactive UI becomes the blocker.

## Limited host-agent slash commands

Treat these as host-agent-facing trigger phrases for this skill, not as Junie’s own interactive slash commands. Keep them conservative and predictable:

- `/junie help` — list these commands and ask for the missing target/path only if needed.
- `/junie status` — inspect install/config/runtime posture without launching a new Junie task; report install state, relevant config locations, current/default model if known, and latest usage availability.
- `/junie model` — report the observed current/default Junie model, provider, and effort sources; do not change config.
- `/junie usage` — summarize latest observable Junie session usage with `python3 scripts/summarize_junie_usage.py --limit 1`; do not launch Junie.
- `/junie bootstrap` — bootstrap or refresh the repo’s Junie-native `.junie/` layout using `scripts/bootstrap_junie_project.py`; preserve existing `.junie/AGENTS.md` unless the user explicitly asks for `--force-agents`.
- `/junie dry-run` — prepare or run a read-only Junie reconnaissance task. Default to `Do not modify files`; use `Open files only; do not run shell commands.` when command execution itself is unwanted.

If a user gives extra words after the command, treat them as the target/scope. If the command is ambiguous or would mutate files/config externally, ask one concise clarifying question before acting.

## 1) Inspect the current state

Check these first:

```bash
command -v junie || true
junie --version || true
printf '%s\n' "$SHELL"
ls -la ~/.junie 2>/dev/null || true
ls -la ./.junie 2>/dev/null || true
ls -la ./.junie/skills 2>/dev/null || true
```

Look for:
- whether Junie is already installed
- whether `~/.local/bin` is on PATH
- whether user-scoped or project-scoped `.junie` config already exists
- whether the repo already has Junie-native directories such as `.junie/skills` or `.junie/AGENTS.md`
- whether the request is local interactive setup or CI/headless setup

Also identify Junie’s model and usage posture and call it out to the user:
- explicit CLI choice you plan to pass (`--model`, `--provider`, `--effort`)
- project/user config model or provider, if present in `.junie/config.json` or `~/.junie/config.json`
- Junie’s current launch model from read-only runtime state, usually `~/.junie/settings.json` keys such as `modelForLaunch` and `effortPerModel`
- after a run, confirm from Junie logs when available; log lines containing `AgentParameters(modelParameters=ModelParameters(model=..., effort=...))` are a useful observed source
- after a run, summarize observable usage when available: model(s), estimated cost, input/output tokens, cache read/write tokens, and any notable helper-model usage

Use the bundled helper from the skill directory for a quick best-effort usage summary:

```bash
python3 scripts/summarize_junie_usage.py --limit 1
```

Do not edit `~/.junie/settings.json` unless explicitly requested. Redact credentials if inspecting config. If the effective model or usage cannot be determined confidently, say `Junie model: unknown` or `Junie usage: unavailable` rather than guessing.

## 2) Install or update Junie

### Preferred install path

Use the bundled helper that matches the shell you are in.

Security/trust posture for publishing:
- Prefer package-manager installs (`brew`, `winget`, `npm`) when they satisfy the request.
- Treat remote installer scripts as higher-trust operations because they download code and execute it locally.
- If you use the official installer path, say so plainly and give the user a chance to review the source URL first when that trust decision matters.

macOS / Linux:

```bash
bash scripts/install_junie.sh
```

Useful variants:

```bash
bash scripts/install_junie.sh --reinstall
bash scripts/install_junie.sh --version 888.169
bash scripts/install_junie.sh --method brew
bash scripts/install_junie.sh --method npm
```

Windows PowerShell:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\install_junie.ps1
```

Useful variants:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\install_junie.ps1 -Reinstall
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\install_junie.ps1 -Version 888.169
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\install_junie.ps1 -Method winget
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\install_junie.ps1 -Method npm
```

### Verification

After install, verify with the platform-appropriate shell.

POSIX shells:

```bash
export PATH="$HOME/.local/bin:$PATH"
junie --version
junie --help
```

PowerShell:

```powershell
junie --version
junie --help
```

Do not claim success until `junie --version` returns cleanly.

## 3) Choose an authentication path

Pick the least interactive path that fits the request.

### Account readiness and first-run failures

When a Junie command fails with account/auth readiness instead of a repo or config result, do not summarize it as a generic blocker. Tell the user what to do next.

Common cases:
- `Authenticated successfully` followed by `Insufficient Account Balance`: Junie is installed and signed in, but the JetBrains Junie account has no usable token balance/credits for CLI runs. Tell the user to open `https://junie.jetbrains.com/cli`, sign in with the intended JetBrains account, check/add CLI credits or generate a fresh CLI token, then rerun with `--auth=<token>` or set `JUNIE_API_KEY`.
- Login/token required, expired, or missing: for normal local desktop usage, first suggest the simplest path: `cd <project-root>` and run `junie` so the interactive first-run/sign-in flow can complete in the project context. For headless/automation, tell the user to visit `https://junie.jetbrains.com/cli`, sign in, generate a CLI token, then either export it temporarily (`export JUNIE_API_KEY='...'`) or pass it once with `junie --auth="$JUNIE_API_KEY" ...`. If the user is still confused or the interactive first-run screen is itself the blocker, offer to drive the `junie` TUI from the project root using `headless-terminal`/PTY control when available; read `references/headless-terminal-fit.md` before doing that.
- BYOK preferred: tell the user to provide/export the relevant provider key (`JUNIE_OPENAI_API_KEY`, `JUNIE_ANTHROPIC_API_KEY`, etc.) and choose the matching `--model`.

If this happens while verifying project guidance, report the partial result clearly: installation/config inspection may be complete, but Junie itself did not execute the assertion because account readiness needs user action.

### A. Headless / CI / automation

Prefer token or provider-key auth.

Junie token:

```bash
export JUNIE_API_KEY='...'
junie --auth="$JUNIE_API_KEY" "summarize this repository"
```

BYOK examples:

```bash
export JUNIE_OPENAI_API_KEY='...'
junie --model gpt-5 "review the latest changes"

export JUNIE_ANTHROPIC_API_KEY='...'
junie --model sonnet "review the latest changes"
```

Use this path when the user asks for CI, scripting, or reliable non-interactive execution.

### B. Interactive local usage

If the user wants normal desktop Junie with browser sign-in or welcome-screen account selection, install Junie first and then let the human complete OAuth unless they explicitly ask you to drive the UI.

Useful command:

```bash
junie
```

### C. Config-file auth defaults

If the user wants persistent defaults, write them into `~/.junie/config.json` or project `.junie/config.json` instead of repeating flags. Put team-shared, non-secret defaults in project config; keep secrets in user config or environment variables unless the user explicitly wants otherwise.

Use the merge helper:

```bash
python3 scripts/merge_junie_config.py ~/.junie/config.json '{"model":"sonnet","auto-update":true}'
```

For BYOK defaults:

```bash
python3 scripts/merge_junie_config.py ~/.junie/config.json '{"provider":"anthropic","byok":{"anthropic":"sk-ant-..."}}'
```

Be careful with secrets:
- prefer environment variables for ephemeral automation
- ask before writing API keys into durable config files
- never overwrite an existing config blindly

## 4) Configure Junie

Junie loads configuration from:
- `~/.junie/config.json`
- `<project>/.junie/config.json`

When bootstrapping a project, prefer the bundled helper so the same conservative layout is created every time:

```bash
python3 scripts/bootstrap_junie_project.py .
python3 scripts/bootstrap_junie_project.py . --model sonnet
python3 scripts/bootstrap_junie_project.py . --config '{"skill-locations":["./skills"]}'
```

The helper creates missing directories, preserves an existing `.junie/AGENTS.md` unless `--force-agents` is passed, and merges `.junie/config.json` instead of replacing it.

Baseline layout:

```text
.junie/
├── AGENTS.md
├── config.json
├── skills/
├── commands/
├── agents/
├── models/
├── mcp/
└── rules/
```

Higher-priority sources override lower-priority ones:
1. CLI flags
2. `~/.junie/settings.json`
3. project `.junie/config.json`
4. user `~/.junie/config.json`

### Common configuration patterns

#### Shared project defaults

Create `<project>/.junie/config.json` when the whole repo should share behavior. Keep paths relative to `.junie/config.json` when possible so the repo stays portable:

```json
{
  "model": "sonnet",
  "skill-locations": ["./skills"],
  "skill-default-locations": true,
  "guidelines-location": "./AGENTS.md",
  "auto-update": true
}
```

#### Personal machine defaults

Create `~/.junie/config.json` for user-specific defaults:

```json
{
  "model": "sonnet",
  "brave": false,
  "auto-update": true,
  "time-limit": 3600
}
```

#### Add external skills or shared folders

Junie already auto-discovers `.junie/skills/`. Add extra paths only when you truly have shared skills outside the standard layout.

```json
{
  "skill-locations": [
    "./skills",
    "/opt/shared/junie-skills"
  ],
  "skill-default-locations": true
}
```

#### Point at a custom guidelines file

```json
{
  "guidelines-location": "./AGENTS.md"
}
```

Only set `guidelines-location` when you need to override discovery. Otherwise let Junie find guidelines naturally. Current documented order includes:
1. custom guidelines filename from `--guidelines-filename` / `JUNIE_GUIDELINES_FILENAME`
2. `.junie/AGENTS.md`
3. `AGENTS.md`
4. `.junie/rules/*.md`
5. legacy `.junie/guidelines.md`

## 5) Steer Junie task quality

Junie is most valuable when it is treated as a dev agent in a managed loop, not merely as a one-shot file generator. For simple one-off tasks, the host agent or Junie can often do the work directly. For higher-value usage, the host agent should act like the project manager/reviewer and Junie like the implementation agent:
- shape the task before handing it off: scope, constraints, acceptance criteria, context commands, and done definition
- keep Junie focused on implementation and local repo operations while the host agent tracks goals, risk, sensitive paths, and verification
- inspect Junie’s result independently, then either accept it, ask a targeted follow-up, or apply small corrections directly
- prefer back-and-forth for exploratory implementation, bug fixing, refactors, or ambiguous repo work; avoid over-orchestrating trivial one-shot artifacts

### Joining an existing host-agent workstream

When Junie joins work that the host agent already understands from prior chat, project notes, an Obsidian-style knowledge base, an issue thread, or another local context index, do not make Junie rediscover all of that context from scratch. Give Junie a compact workstream handoff:
- current goal and why Junie is being brought in
- known state in 5-10 concrete bullets
- open decisions or hypotheses to test
- exact files/directories Junie should inspect first
- whether the first pass is read-only, plan-only, or allowed to edit
- output shape the host agent needs for review
- model and usage posture: observed current/default Junie model when known, any explicit `--model`/`--provider`/`--effort` override, stronger model recommendation if relevant, and post-run observable usage/cost if available

For read-only reconnaissance, say `Do not modify files` and also constrain shell posture if needed. Junie may still use harmless read-only shell commands unless explicitly told not to; if command execution itself is unwanted, say `Open files only; do not run shell commands.`

Critical steering rule: do not assume Junie inherits the host agent’s understanding of the project just because that context exists elsewhere. If the task depends on project doctrine, local vocabulary, current constraints, or medium-specific expectations, restate that context explicitly in the Junie task.

In practice, front-load the brief with the context Junie actually needs to succeed:
- what the project is, in plain language
- what file(s) or subsystem(s) matter
- what truths are canonical versus metaphorical
- what is explicitly out of scope
- what failure would look like
- what a successful result should change, and what must stay untouched

Be especially explicit when the work carries non-obvious project doctrine or domain priors that Junie may otherwise fill in incorrectly. Examples:
- domain-specific vocabulary (`customer` vs `tenant`, `case` vs `ticket`, `workspace` vs `project`)
- platform or framework constraints (supported runtime, deployment target, storage model, permissions model)
- project-specific invariants, safety rules, or compatibility promises
- naming that looks familiar but means something narrower in this repo than in generic software usage

When a task is likely to trigger generic priors, say so directly and pin Junie to the local truth. Good steering often sounds like:
- `Do not assume the generic framework defaults apply; this repo wraps request handling through the project-specific adapter in <file>.`
- `Treat the current public API as the compatibility boundary; prefer internal refactors over changing exported behavior unless explicitly requested.`
- `The host agent knows the broader project history, but you should rely only on the context explicitly given here plus the listed files.`

Also steer explicitly around write posture. If Junie is not in Brave Mode, or if the task touches important existing files, do not assume it will confidently mutate them just because the user asked the host agent. Say what it is allowed to edit and, when helpful, whether a derived output file is preferred.
- name the exact file(s) Junie may change
- say whether it should modify in place or create a sibling/derived file first
- if conservatism is desirable, prefer `create exactly one new file` over an ambiguous in-place rewrite
- if in-place mutation is required, say so plainly instead of implying it

Treat Junie runs as expensive. Model quota, patience, and review attention are all finite. Prefer fewer, sharper runs over exploratory churn.
- front-load the real scope and doctrine into one brief rather than spending multiple paid runs rediscovering context
- collapse reconnaissance when the host agent already has the answer; pass Junie the relevant conclusions and file list
- prefer one decisive implementation pass plus one follow-up correction over a long chain of vague attempts
- when a run is drifting into re-reading and re-deriving, tighten the task or stop and retry with a narrower brief
- if a cheaper artifact would de-risk the real task (for example a derived file or a doctrine-alignment doc pass), use that deliberately rather than by accident

Do not assume Junie’s own suggested tasks will produce good output with default prompting/model settings. For quality-sensitive work, especially synthesis from repo history or source context:
- call out which Junie model/effort is currently in use or planned before reporting/starting meaningful runs; include the source when useful, e.g. `Junie model observed: claude-opus-4-7, effort low (from ~/.junie/settings.json / latest Junie log)`
- after each meaningful run, call out observable Junie usage when available; keep it compact, e.g. `Junie usage observed: $0.027318; claude-opus-4-7 + helper models; 1,931 input / 430 output / 16,890 cache-read / 1,330 cache-write tokens`
- choose or recommend a stronger model/effort before blaming the task itself
- explain model tradeoffs plainly when they matter: quality, speed, availability, and likely quota/billing weight
- for quick dry-runs, use the current/default Junie model unless the user already chose a model or the task clearly needs escalation
- treat the user as the final decision-maker for model selection, especially for substantial runs on expensive or scarce models
- give explicit acceptance criteria, desired depth, and output shape
- provide the exact context command when possible, e.g. `git log -5 --stat --summary` instead of vague “last 5 commits”
- verify the artifact yourself before reporting success; if output is shallow, say so and either retry with better steering/model or fix it directly

## 6) Verify configuration

Use the lightest check that proves the requested state.

### Install only

```bash
junie --version
junie --help
```

### Headless auth

If a token is available, run a tiny non-destructive prompt in a throwaway project or harmless directory:

```bash
junie --auth="$JUNIE_API_KEY" --task "Say hello and report the current working directory" --output-format text
```

### Config merge or project bootstrap

Read back `.junie/config.json` or `~/.junie/config.json` and confirm only the intended keys changed. Do not silently replace unrelated discovery paths, provider defaults, or BYOK entries.

For project bootstrap, also confirm the expected directories exist and that an existing `.junie/AGENTS.md` was preserved unless overwrite was explicitly requested.

## 7) Decide whether `headless-terminal` is needed

Usually: no.

Treat Junie CLI/TUI ↔ IDE integration as aspirational unless the current environment proves otherwise. The CLI exposes hints such as `--acp` for IDE integrations, `--ide-guidelines`, and `~/.junie/settings.json` may contain `connectToIde`, but do not assume the IDE side is actually active, visible, or useful. Prefer standalone CLI behavior and repo-local files as the reliable integration surface.

Junie exposes enough non-interactive control for installation and configuration:
- installer script
- `--auth`
- provider API key flags
- environment variables
- `config.json`

Use `headless-terminal` only when all of these are true:
- the user explicitly wants the interactive Junie UI driven by the agent, or a setup step exists only in the TUI
- plain `exec`/`process` control is too brittle because the UI redraws, uses alternate screen buffers, or waits for keystroke-driven menus
- there is no equivalent flag, env var, or config-file route

Observed practical rule from local Junie safari:
- plain `exec`/`process` PTY control is good enough when Junie behaves like a transcript-emitting interactive CLI and you only need progress text or a simple prompt/response loop
- `headless-terminal` becomes worthwhile when you need the rendered screen itself to be legible and stable, especially command menus, `/usage`, `/model`, help overlays, or other palette-like UI states

Typical `ht`-worthy cases:
- navigating the welcome screen
- driving `/account` or `/model` inside Junie interactively
- inspecting `/usage` or other slash-command surfaces where screen layout matters
- capturing a stable snapshot of the Junie TUI for debugging

Non-`ht` cases:
- running the installer
- writing config files
- passing `--auth` or env vars
- headless CI usage
- ordinary Junie task execution where the transcript already reports opened files, edits, and task results

If you do need `ht`, read `references/headless-terminal-fit.md` and use the separate `headless-terminal` skill.

## References

- `references/junie-doc-notes.md`: distilled install, auth, config, directory-layout, and verification notes from Junie docs
- `references/headless-terminal-fit.md`: decision rule for when interactive PTY tooling is worth it
- `scripts/install_junie.sh`: POSIX-shell wrapper around official install methods
- `scripts/install_junie.ps1`: PowerShell wrapper around official Windows install methods
- `scripts/merge_junie_config.py`: conservative JSON merge helper for Junie config files
- `scripts/bootstrap_junie_project.py`: conservative `.junie/` project-layout bootstrap helper
