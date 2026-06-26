---
name: prompt-ab-lab
description: Design, log, compare, and score prompt experiments so users can systematically
  improve outputs instead of guessing.
version: 1.1.0
metadata:
  openclaw:
    requires:
      bins:
      - python3
    emoji: 🧰
---

# Prompt A/B Lab

## Purpose

Design, log, compare, and score prompt experiments so users can systematically improve outputs instead of guessing.

## Trigger phrases

- 比较两个提示词
- prompt ab test
- 提示词实验
- 哪个 prompt 更好
- 建一个评测表

## Ask for these inputs

- prompt A and B
- task
- evaluation criteria
- test set
- weights if any

## Workflow

1. Define what success looks like before comparing prompts.
2. Generate an evaluation rubric and structured test table.
3. Log outputs per test case and compute weighted scores.
4. Summarize tradeoffs instead of declaring a winner too early.
5. Recommend the next experiment iteration.

## Output contract

- experiment plan
- scored comparison table
- rubric
- next-iteration suggestions

## Files in this skill

- Script: `{baseDir}/scripts/prompt_experiment_logger.py`
- Resource: `{baseDir}/resources/eval_rubric.md`

## Operating rules

- Be concrete and action-oriented.
- Prefer preview / draft / simulation mode before destructive changes.
- If information is missing, ask only for the minimum needed to proceed.
- Never fabricate metrics, legal certainty, receipts, credentials, or evidence.
- Keep assumptions explicit.

## Suggested prompts

- 比较两个提示词
- prompt ab test
- 提示词实验

## Use of script and resources

Use the bundled script when it helps the user produce a structured file, manifest, CSV, or first-pass draft.
Use the resource file as the default schema, checklist, or preset when the user does not provide one.

## Boundaries

- This skill supports planning, structuring, and first-pass artifacts.
- It should not claim that files were modified, messages were sent, or legal/financial decisions were finalized unless the user actually performed those actions.


## Compatibility notes

- Directory-based AgentSkills/OpenClaw skill.
- Runtime dependency declared through `metadata.openclaw.requires`.
- Helper script is local and auditable: `scripts/prompt_experiment_logger.py`.
- Bundled resource is local and referenced by the instructions: `resources/eval_rubric.md`.
