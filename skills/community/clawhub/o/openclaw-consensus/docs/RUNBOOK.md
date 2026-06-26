# Runbook

## Purpose
This file explains the practical build and validation order for the current `openclaw-consensus` MVP.

## Current reality
This repo now contains:
- a real local `SKILL.md`
- a repo-local runtime in `src/cli.mjs`
- local install/uninstall scripts
- validation evidence for install, uninstall/reinstall, happy path, failure path, and tracked-file safety

It still does not contain:
- domain presets
- web UI
- local-model routing
- skill-hub packaging beyond repo structure/readiness

## Build and validation order
1. keep README and `docs/COMMANDS.md` truthful
2. install the local skill into the workspace
3. verify `openclaw skills info openclaw-consensus`
4. inspect configured API-backed models
5. run the happy path
6. run one failure path
7. inspect `run.json` and `final.md`
8. tighten public repo readiness only after evidence stays clean

## First implementation slice that now exists
The repo already has the smallest runnable local skill path:
- repo-local skill source
- documented local install flow
- documented local uninstall flow
- one narrow runtime entrypoint
- deterministic artifact output location

## Release-prep rule
Do not treat the repo as release-ready unless all of these still hold:
- local skill install works
- local skill uninstall works
- one end-to-end sample run works
- one failure path is tested
- tracked-file safety check is clean

## Anti-drift rule
If implementation reality changes, update:
- `README.md`
- `docs/COMMANDS.md`
- `docs/SKILL_LIFECYCLE.md`
- the active task artifact
- `validation/` evidence when release claims depend on it

The repo story must stay aligned with the code and proof, not old plans.
