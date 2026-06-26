# OpenClaw Consensus

Focused OpenClaw-native skill and repo-local CLI for fixed 2-round cross-model deliberation.

## What this is
OpenClaw Consensus runs one brief through 2-4 explicitly selected API-backed models from the active OpenClaw-configured pool, gives them one shared reconciliation round, and then writes a final synthesis covering:
- consensus
- disagreements
- uncertainty
- narrow escalation points

This repo is intentionally small. It is a **local OpenClaw skill + CLI runtime**, not a SaaS, not a hosted workflow, and not a claim that model agreement replaces expert judgment.

## MVP boundaries
- exactly 2 rounds
- generic workflow only
- explicit model shortlist required
- selected models must come from the active OpenClaw-configured pool
- no `ollama/*` routing in this MVP
- orchestrator model should be the current OpenClaw session model
- no expert-replacement framing

## Repo shape
- `SKILL.md` — local OpenClaw skill instructions
- `src/cli.mjs` — repo-local runtime and CLI
- `scripts/install-skill.sh` — dev install via workspace copy
- `scripts/uninstall-skill.sh` — dev uninstall flow
- `docs/` — product/runtime/prompt/artifact contracts
- `tasks/` — execution artifacts and project history
- `validation/` — captured proof for release claims

## Quick start
### 1. Install the local skill into this workspace
```bash
./scripts/install-skill.sh
openclaw skills info openclaw-consensus
```

### 2. Inspect the configured API-backed model pool
```bash
node src/cli.mjs models
```

### 3. Run one consensus pass
```bash
node src/cli.mjs run \
  --brief "Compare the tradeoffs of postponing a database migration by one quarter versus doing it now." \
  --models "openai-codex/gpt-5.4,openai-codex/gpt-5.5" \
  --orchestrator-model "openai-codex/gpt-5.4" \
  --label "migration-tradeoff"
```

### 4. Inspect artifacts
```text
runs/<timestamp>-<slug>/
├── brief.md
├── run.json
├── round-1/
├── round-2/
└── final.md
```

### 5. Remove the local skill link when finished
```bash
./scripts/uninstall-skill.sh
```

## Validation status
This repo includes captured proof for:
- local install
- local uninstall + reinstall
- model-pool inspection
- one end-to-end happy-path run
- one failure-path run that rejects provider fallback
- tracked-file safety check

See `validation/2026-04-29/` for the recorded outputs.

## Security / secret posture
- provider keys are **not** stored in this repo
- runtime outputs live under `runs/`, which is gitignored by default
- public validation artifacts were checked for tracked secret patterns and scrubbed of machine-local absolute paths where needed

## Hardening posture
The CLI applies a small set of conservative guardrails. These are belt-and-suspenders, not a sandbox:
- prompts fence the brief and round outputs with a per-run random nonce so that user-supplied content cannot trivially terminate the fence
- each model call runs under a per-call timeout (`--model-timeout-ms`, default 5 minutes)
- default run directories under `runs/` use collision-safe creation (suffix `-2`, `-3`, …) instead of clobbering
- explicit `--run-root` is rejected if it points at common system paths or at a non-empty directory
- `run.json` truncates and redacts the brief from any persisted error message
- the run-time check that openclaw executed the requested model (not a fallback) is the authoritative protection against silent provider substitution

See `validation/tests/` for offline regression tests covering these helpers,
prompt structure, run-directory creation, and CLI-boundary argument handling.
Run them with `npm test` (or `./scripts/run-tests.sh`). The offline suite does
not invoke `openclaw` and does not consume API credit; live end-to-end runs
are documented in `docs/COMMANDS.md` and must be invoked explicitly.

## Notes on the orchestrator model
The repo contract says the orchestrator should use the current OpenClaw session model. When the skill is used from chat, the agent should pass that model explicitly to the CLI. For standalone shell use, the CLI falls back to the workspace agent primary model if `--orchestrator-model` is omitted, and records that source in `run.json`.

## What this repo does not do
- no domain presets
- no web UI
- no local-model routing
- no extra rounds
- no automatic trust in consensus

## Status
This is a real, usable MVP. The point is not feature sprawl; the point is a truthful, inspectable, artifact-first consensus workflow that is already useful inside OpenClaw.
