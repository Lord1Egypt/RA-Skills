# Skill Lifecycle

## Purpose
Define the actual lifecycle now implemented for `openclaw-consensus`.

## Phase 1 — Local workspace skill
This repo now works as a real local workspace skill.

Current shape:
- repo root contains `SKILL.md`
- `scripts/install-skill.sh` copies the repo into `<workspace>/skills/openclaw-consensus`
- `scripts/uninstall-skill.sh` removes only a repo-owned installed copy marked for this dev flow
- `src/cli.mjs` provides the runtime entrypoint used by the skill

## Local lifecycle
### Find
From this repo:
```bash
./scripts/install-skill.sh
openclaw skills info openclaw-consensus
```

### Install
Development install is a workspace copy created by `rsync`, not a symlink.
OpenClaw rejects workspace-skill symlink escapes, so the repo uses a guarded copy flow instead.

### Configure
Configuration stays in OpenClaw:
- provider/model auth remains OpenClaw-owned
- configured model visibility comes from `openclaw config get agents`
- the repo does not add a second provider-auth layer

### Invoke
The runtime is repo-local:
```bash
node src/cli.mjs run --brief "..." --models "model-a,model-b"
```

When used through the installed skill, the agent should pass the current session model as `--orchestrator-model`.

### Check status
Status exists in two places:
- `openclaw skills info openclaw-consensus` for skill visibility
- run artifacts (`run.json`, `round-1/`, `round-2/`, `final.md`) for execution status

### Remove
```bash
./scripts/uninstall-skill.sh
```

The uninstall flow refuses to remove a target that does not carry the repo install marker.

## Phase 2 — Public repo quality
Public readiness now depends on evidence, not claims.
Minimum proof:
- install works
- uninstall works
- reinstall works
- one happy-path run works
- one failure path is captured
- tracked-file safety check is clean

## Phase 3 — Skill hub targeting
This repo is structured so ClawHub-style packaging is natural later, but hub submission is still a later step.
The current truth is:
- the local skill path is real
- the repo-local runtime is real
- validation evidence exists
- no hub-specific packaging has been claimed or added yet

## Rule
Do not widen the lifecycle story beyond what this repo can prove locally today.
