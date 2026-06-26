---
name: modelpilot
description: Use this skill when the user wants to test, compare, promote, replace, or clean up local Ollama models with a repeatable two-round real-task benchmark, no-think verification, and local-only safety boundaries. It applies to local LLM evaluation, model replacement decisions, benchmark reports, installed-model audits, and Ollama workflow hygiene. Do not use it for cloud model APIs, downloading models, installing dependencies, or sending local data outside the machine.
---

# ModelPilot

ModelPilot is a local-only protocol for testing, comparing, promoting, replacing,
and cleaning up Ollama models. It is designed for real work decisions, not leaderboard
claims.

## Safety Boundary

Always keep the workflow local unless the user explicitly authorizes otherwise.

- Do not call cloud model APIs.
- Do not upload files, prompts, logs, paths, configs, or benchmark outputs.
- Do not download, pull, install, upgrade, or delete models without explicit user approval.
- Do not use real private documents as benchmark samples unless the user explicitly names the file for this task.
- Use fictional examples for tests, documentation, and demos.
- Treat model cleanup as a workflow dependency audit, not a disk-space optimization task.

## Trigger Conditions

Use this skill when the user asks to:

- test an Ollama model
- compare local models
- decide whether a new model can replace an existing model
- verify no-think behavior
- build a local model benchmark report
- audit installed models before cleanup
- choose local models for coding, writing, RAG, automation, or structured output

## Test Levels

Classify the task before running anything.

1. Smoke Test
   Confirm the model is installed, runnable, and responsive.

2. Speed Benchmark
   Measure startup time, generation time, output length, and failure rate.

3. Real-Task Benchmark
   Use task-like prompts that match the user's actual workflow. Prefer fixed prompt
   sets so results are comparable across models.

4. Promotion Test
   Decide whether a model can replace an existing workflow model. A promotion test
   requires two independent benchmark rounds.

## Two-Round Replacement Rule

Do not recommend replacing a working model after a single run.

- Round 1 checks: runnable, speed, output format, obvious quality failures, no-think leakage.
- Round 2 checks: same prompt set, same model, repeatability, quality consistency, failure modes.
- A model is only replacement-ready when both rounds pass the required tasks.
- Keep the previous model and configuration available for rollback.
- If structured output, no-think behavior, or long-context handling is unstable, do not use the model in automation.

## Fixed Prompt Set

Prefer a stable prompt file with fictional data. Include at least:

- short Chinese or English Q&A
- long-document summary
- structured JSON or Markdown output
- real-role workflow simulation
- no-think verification prompt

The benchmark prompt set should be reused across candidate models. Do not compare
models using different tasks unless the report clearly says so.

## No-Think Verification

Never assume a model is no-think just because the model name contains `nothink`.

Check:

- model output does not include `<think>`, `</think>`, reasoning traces, or hidden-analysis markers
- CLI or API flags are actually accepted by the runtime
- Modelfile-level instructions are treated as weak constraints, not proof
- structured outputs remain clean when no-think is enabled

If no-think fails, the model may still be useful for manual work, but it should not
be promoted into automated workflows that require clean output.

## Standard Workflow

1. Identify the current model, candidate model, task type, and replacement target.
2. Confirm whether the user wants smoke, speed, real-task, or promotion testing.
3. Build or reuse a fixed prompt set with fictional data unless the user explicitly authorizes a real file.
4. Run two benchmark rounds for replacement decisions.
5. Review mechanical results: failures, duration, output length, format checks, no-think leakage.
6. Review semantic quality manually for real-task tasks.
7. Return a concise decision: keep, observe, replace, or not recommended.
8. Include rollback advice when replacement is recommended.

## Suggested Local Scripts

Use scripts only when they are available in this skill folder and fit the task.

- `scripts/modelpilot_benchmark.py`: run local Ollama benchmark rounds and write JSON results.
- `scripts/modelpilot_report.py`: summarize benchmark JSON into a Markdown decision report.

Do not run scripts that download models, install dependencies, or call remote APIs.

## Required Response Format

When reporting results, include:

```markdown
## ModelPilot Result

### Scope
-

### Models Tested
-

### Test Rounds
-

### Key Findings
-

### No-Think Check
-

### Replacement Decision
-

### Risks and Limits
-

### Rollback Advice
-
```

