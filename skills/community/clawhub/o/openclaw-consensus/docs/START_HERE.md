# Start Here

Use this checklist to align `openclaw-consensus` before deeper implementation work.

## 1. Confirm the product boundary
The repo is for:
- a focused OpenClaw-native skill
- fixed 2-round cross-model deliberation
- generic-only MVP
- public-quality repo and future skill-hub targeting

It is not for:
- web UI
- domain modes in MVP
- local model routing in MVP
- execution workflows

## 2. Confirm configuration assumptions
- OpenClaw owns provider/model auth and availability
- the skill selects explicitly from the OpenClaw-configured model pool
- no default model selection in MVP
- orchestrator model = current OpenClaw session model

## 3. Confirm prompt invariance rules
- round 1 brief is passed 1:1 unchanged to all selected answer models
- round 2 prompt is identical across all selected answer models
- round 2 includes one merged quoted/delimited block of all round-1 answers

## 4. Keep the repo truthful
Before adding implementation:
- remove misleading template residue
- keep `docs/COMMANDS.md` honest
- keep README concise and public-facing
- keep task artifacts current

## 5. Build in the right order
1. docs and repo boundary
2. skill source layout + local install/uninstall flow
3. runtime skeleton
4. happy-path validation
5. failure-path validation
6. public release tightening

## 6. Do not rush public claims
The repo should not be presented publicly as a real skill until:
- the local skill path works
- validation evidence exists
- the release checklist is clean
