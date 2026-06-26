---
name: openclaw-consensus
description: Run a fixed 2-round cross-model deliberation through the repo-local OpenClaw Consensus runtime.
metadata: {"openclaw":{"emoji":"🧭","requires":{"bins":["node","openclaw"]}}}
---

# OpenClaw Consensus

Use this skill when the user explicitly wants a bounded cross-model deliberation on one brief.

## What this skill does
- runs the same brief through 2-4 explicitly selected API-backed models from the active OpenClaw-configured pool
- preserves round-1 and round-2 artifacts on disk
- asks the current session model to write the final synthesis

## Do not use this skill when
- the user wants casual chat or a single quick answer
- the user did not agree to explicit model selection yet
- the request is framed as replacing a lawyer, accountant, doctor, engineer, or other expert

## Required inputs
Before running, confirm all of these:
1. one final brief
2. an explicit model shortlist of at least 2 models
3. an optional run label if the user wants one

## Model rules
- In this MVP, the model shortlist is required.
- Only use models that appear in `node {baseDir}/src/cli.mjs models`.
- Do not silently substitute a missing or failing model.
- Do not use `ollama/*` models in this repo's MVP.

## Invocation flow
1. If needed, inspect the configured model pool:
   ```bash
   node {baseDir}/src/cli.mjs models
   ```
2. Run the consensus flow with the brief, explicit model list, and the current session model as orchestrator:
   ```bash
   node {baseDir}/src/cli.mjs run --brief "<brief>" --models "openai-codex/gpt-5.4,openai-codex/gpt-5.5" --orchestrator-model "<current-session-model>" --label "optional-label"
   ```
3. Read back the generated `final.md` and `run.json` before summarizing for the user.

## Output expectations
Read the final synthesis carefully and present it truthfully:
- consensus
- disagreements
- unresolved uncertainty
- escalation points
- best overall synthesis

## Safety rules
- Preserve disagreement; do not flatten it in your summary.
- Consensus is not proof of correctness.
- Keep expert-escalation language narrow and honest.
- If the CLI reports a fallback or unavailable selected model, stop and surface the failure clearly instead of improvising around it.
