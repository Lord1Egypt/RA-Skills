# AI Bootstrap Guide

This file tells a future AI/operator how to enter `openclaw-consensus` without drifting the product boundary.

## Read order for AI
Before acting on meaningful work, read:
1. `README.md`
2. `AGENTS.md`
3. `docs/PRINCIPLES.md`
4. `docs/PRODUCT_SPEC.md`
5. `docs/RUNTIME_CONTRACT.md`
6. `docs/PROMPT_CONTRACT.md`
7. `docs/OUTPUT_TEMPLATE.md`
8. `docs/COMMANDS.md`
9. the active task file in `tasks/`
10. `validation/` evidence if you are making public-readiness claims

## Project reality
This repo now contains a real local skill + runtime MVP:
- fixed 2-round workflow
- generic-only MVP
- explicit answer-model shortlist from the OpenClaw-configured pool
- no default answer-model selection
- repo-local CLI runtime in `src/cli.mjs`
- repo-local install/uninstall flow via guarded workspace copy
- fallback rejection if OpenClaw executes a different model than requested

## First duty in this repo
Preserve truthfulness:
- keep README concise and public-quality
- keep `docs/COMMANDS.md` limited to commands that really exist
- keep product/runtime docs aligned with implementation reality
- update task artifacts and validation evidence when reality changes

## Operating shape
For nontrivial work, use:
- `[RESTATE]`
- `[PLAN]`
- `[STATUS]`
- `[DONE]`
- `[BLOCKED]`

## What must not drift
- this project is a skill first, not a web app
- MVP is exactly 2 rounds
- no domain modes in MVP
- no duplicate provider auth/config inside this repo
- no `ollama/*` routing in this MVP
- no expert-replacement framing
- no public claims without validation evidence

## Public-release posture
The target is:
- a real working local skill
- a clean GitHub repo
- credible future skill-hub submission

Do not claim skill-hub compatibility beyond the repo structure and local proof that already exist.

## Good future prompts
### Prompt: continue implementation
```text
Read README.md, AGENTS.md, docs/PRINCIPLES.md, docs/PRODUCT_SPEC.md, docs/RUNTIME_CONTRACT.md, docs/PROMPT_CONTRACT.md, docs/OUTPUT_TEMPLATE.md, docs/COMMANDS.md, the active task file, and relevant validation evidence.
Then restate the objective, make a plan, and execute only within the locked product boundary.
```

### Prompt: prepare public release
```text
Audit the repo for public release readiness.
Do not add features.
Tighten only docs, packaging, validation evidence, safety, and public-facing clarity.
Surface any tracked-file risk or misleading claim before release.
```

### Prompt: validate the skill
```text
Run the documented validation path for openclaw-consensus.
Prove install/uninstall, invocation, happy path, and one failure path.
Do not claim the repo is release-ready without evidence.
```
