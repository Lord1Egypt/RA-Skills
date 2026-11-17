---
name: model-inventory
description: Scan the machine for installed AI coding CLIs (claude, codex, gemini, copilot, opencode, ollama), detect whether each account is actually active and which models are usable, and cache the result to ~/.claude/model-inventory.json with role→model routing chains (planner/coder/scout/reviewer/fixer) that goal-runner and autopilot consume to pick the best available model per sub-agent while staying cost-efficient. Three evidence tiers — installed (binary found), likely-authenticated (zero-token credential heuristics), verified (a live one-line probe per model, the only ground truth for "account active and model on the plan"). Use this skill whenever the user says "scan available models", "which models can I use", "what AI CLIs are installed", "refresh the model inventory", "is fable available", "check my model access", or "/model-inventory" — even if they don't name the skill. Not for picking a model mid-task (consumers read the cached file, they don't rescan).
---

# Model Inventory

Scan → probe → cache: which AI CLIs live on this machine, which models each can *actually* use right now, and a role→model routing table other skills consume to spawn each sub-agent on the best model available — strongest for planning, cheapest that suffices for mechanical work.

## When to use this skill

- "scan available models" / "which models can I use" / "check my model access"
- "what AI CLIs are installed" / "is fable available"
- "refresh the model inventory" / "/model-inventory"
- A consumer skill (goal-runner, autopilot, task-executor) finds `~/.claude/model-inventory.json` missing or stale at kickoff and invokes this skill to rebuild it

Do **not** auto-trigger mid-task to choose a model — consumers read the cached inventory; rescanning is this skill's explicit job.

## Evidence tiers

| Tier | How | Cost | Proves |
|---|---|---|---|
| 1 `installed` | `scripts/scan.sh`: `command -v` + `--version` | zero tokens | the binary exists |
| 2 `likely-authenticated` | scan.sh credential heuristics (file/env *names*, never values) | zero tokens | credentials exist — **not** that the account is active or the plan covers a model |
| 3 `verified` | one live probe per model ([references/cli-registry.md](references/cli-registry.md)) | a few tokens per model | account active AND model on the plan |

The rule consumers rely on: **a model status not observed from a live probe is `unverified`, never `verified`.** An expired subscription looks identical to an active one until tier 3 — that's the whole reason tier 3 exists.

- ❌ "claude is installed and has credentials, so fable: verified" — the plan may not include fable; that's an entitlement error only a probe surfaces.
- ✅ `fable: verified — probe replied "ok"` or `fable: unavailable — "Error: model not available on your plan"` (quoted).

## Workflow

1. **Tiers 1–2 — run the scan.** Execute `scripts/scan.sh` (bash; runs on Git Bash/macOS/Linux) and show the user the per-CLI result. Zero tokens spent, nothing sent anywhere.
2. **Tier 3 — probe, unless the user said "quick scan".** For each installed CLI, run the probe command from [references/cli-registry.md](references/cli-registry.md) once per seed model (claude: all four aliases; other CLIs: `default` only) and classify by the table there: `verified` / `unavailable` / `blocked-by-auth` / `quota-exhausted` / `unknown`. A login error flips the CLI's `auth.status` to `unauthenticated` and marks all its models `blocked-by-auth` — the "installed but account not active" case, with the error line quoted. A timeout is `unknown`, never `unavailable`. One attempt per model; retry once only after changing one named thing; second failure → record `unknown` with the quoted error and move on. Ollama needs no probe — `ollama list` already verified its models locally.
3. **Build the routing table** per the rules below, from probe results only.
4. **Write `~/.claude/model-inventory.json`** (schema below), then report: a per-CLI table (version, auth status, each model's status with evidence), what was probed vs. assumed, and total probe cost. Zero usable CLIs is a valid outcome — write the inventory anyway so consumers see an honest empty rather than a missing file.

## Routing rules

`routing.agent_tool` holds fallback chains of **claude aliases only** (haiku/sonnet/opus/fable — never dated model ids, they rot; sub-agents spawned via the Agent tool ride the current session's auth). Start from the canonical chains, then delete any alias whose probe said `unavailable` or `blocked-by-auth`; never reorder:

```json
{
  "planner":         ["fable", "opus", "sonnet"],
  "coder":           ["sonnet"],
  "coder_high_risk": ["fable", "opus", "sonnet"],
  "scout":           ["haiku", "sonnet"],
  "reviewer":        ["opus", "sonnet"],
  "fixer":           ["sonnet"]
}
```

The cost policy lives in the shape: the strongest model is the *escalation* (planning, high-blast-radius coding, review adjudication), never the default for mechanical work. `routing.bash_workers` lists non-claude CLIs whose `default` probe verified — candidates for shell-invoked delegation, not Agent-tool spawns.

## Consumption contract

- File: `~/.claude/model-inventory.json`. Top level: `schema`, `generated_at` (UTC ISO), `platform`, `probed` (bool), `clis[]` (name, installed, path, version, `auth{status,evidence}`, invocation, optional `default_model{id,evidence}` from the CLI's local config, `models[]{id,status,evidence}` where a `default` entry carries `resolved_id` when the probe banner revealed what actually ran), `routing{agent_tool, bash_workers}`.
- Consumers take the **first** entry of a role's chain not marked `unavailable`/`blocked-by-auth`/`quota-exhausted` and pass it as the Agent tool's `model` param — bare aliases only; skip any other value. Missing, unparseable, `generated_at` older than 7 days, or `probed: false` → treat as absent: spawn with no model override and optionally suggest rerunning this skill. Never let a stale inventory block work, and never hand-write this file from a consumer — it's this skill's artifact. Consumers with this skill installed may invoke it **once at kickoff** to rebuild a missing/stale inventory (logging the discovery run), and may rerun `scripts/scan.sh` as a free sanity check anytime — but never probe mid-run; mid-run model failures are the consumer's chain-fallback problem, not a rescan trigger.

## Examples

### Example 1: full scan

**User:** "scan available models"

**Claude:** runs `scan.sh` (finds claude + codex installed, both likely-authenticated; gemini not installed), probes claude's four aliases (haiku/sonnet/opus verified; fable → `unavailable`, quoted: "not available on your plan") and codex's default (verified), writes the inventory with `planner: ["opus","sonnet"]` (fable deleted per probe), reports the table + ~$0.03 probe cost.

### Example 2: installed but account inactive

**User:** "refresh the model inventory"

**Claude:** scan shows codex installed with `~/.codex/auth.json` present (tier 2: likely-authenticated). The tier-3 probe returns "Not logged in — run codex login". Inventory records `auth.status: "unauthenticated"` with that line quoted, `default: blocked-by-auth`, and codex is left out of `bash_workers`. The report tells the user `codex login` would restore it — the skill never runs login flows itself.

## Anti-patterns

- ❌ Marking a model `verified` because the CLI is installed or credentials exist — tier 2 cannot see expired subscriptions or plan entitlements.
- ❌ Recording a probe timeout as `unavailable` — a flaky network would silently delete your best model from every chain. Timeout = `unknown`, chain keeps the alias.
- ❌ Writing credential *values* into evidence — name the signal ("env OPENAI_API_KEY is set"), never print the key.
- ❌ Putting dated model ids in `agent_tool` chains — aliases only; ids rot and consumers pass these straight into spawns.
- ❌ Re-probing in a loop until a model "comes back" — one attempt, one named-change retry, done.
- ❌ Running `codex login` / auth flows to "fix" an inactive account — report it; the login is the user's move.
- ✅ Scan free, probe once with quoted evidence, write the inventory, report what's verified vs. assumed vs. blocked.

## Notes

- Composes with `goal-runner`, `autopilot`, and `task-executor` as consumers (they resolve each sub-agent role from `routing.agent_tool` when the inventory is fresh, invoke this skill once at kickoff to rebuild it when it's missing or stale, and degrade to no-override when this skill isn't installed or discovery fails). This skill owns discovery and the file format; consumers never probe mid-run.
- To cover another CLI, follow "Adding a CLI" in [references/cli-registry.md](references/cli-registry.md) — one auth heuristic in `scan.sh`, one registry section.
- Ollama models are free to run but weak as coding workers — they land in `bash_workers` with their evidence; consumers decide whether local quality suffices.
