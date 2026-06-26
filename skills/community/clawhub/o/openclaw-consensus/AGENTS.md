# AGENTS.md — Project Operating Contract

## First Read Order
Before doing meaningful work in this repo, read in this order:
1. `README.md`
2. `docs/PRINCIPLES.md`
3. `docs/PRODUCT_SPEC.md`
4. `docs/RUNTIME_CONTRACT.md`
5. `docs/PROMPT_CONTRACT.md`
6. `docs/OUTPUT_TEMPLATE.md`
7. `docs/COMMANDS.md`
8. the active file in `tasks/`

## Repo Purpose
This repo exists to build `openclaw-consensus` as a focused OpenClaw-native skill for 2-round cross-model deliberation, with a quality public repo and future official skill-hub targeting.

## Locked Product Rules
- fixed 2-round workflow
- generic-only MVP
- answer models selected explicitly from the OpenClaw-configured pool
- no default model selection in MVP
- orchestrator model = current OpenClaw session model
- round 1 brief passed 1:1 unchanged to all answer models
- round 2 prompt identical across all answer models
- no expert-replacement framing

## Working Rules
- Restate before nontrivial execution.
- Make a numbered plan for multi-step work.
- Create or update a task file in `tasks/` for meaningful work.
- Validate against the objective, not just syntax.
- Update docs when reality changes.
- Keep commits meaningful.
- Do not widen scope silently.

## Minimum Execution Shape
Use these blocks for nontrivial work:
- `[RESTATE]`
- `[PLAN]`
- `[STATUS]`
- `[DONE]`
- `[BLOCKED]`

## Repo Hygiene
- `README.md` must stay accurate and public-quality.
- `docs/COMMANDS.md` should contain only the real command surface.
- Product/runtimes docs must stay aligned with implementation reality.
- `tasks/` should preserve execution context that should survive chat resets.
- Template-era wording should be removed once misleading.

## Release Discipline
Do not treat the skill as publicly real until there is evidence for:
- local install/uninstall
- invocation path
- happy-path run
- failure-path handling
- tracked-file safety

## Safety
- Ask before destructive actions.
- Do not expose secrets.
- Keep the repo understandable by a future fresh session.
- Do not claim that model consensus replaces expert judgment.
