---
name: improvement-evaluator
description: "当需要验证 Skill 改进是否真正提升了 AI 执行效果时使用。通过预定义任务集（YAML）运行 AI 任务，判定 pass/fail，输出 execution_pass_rate。不用于文档结构评分（用 improvement-learner）或候选打分（用 improvement-discriminator）。"
license: MIT
triggers:
  - evaluate skill execution
  - run task suite
  - execution pass rate
  - 执行效果评估
  - 任务集验证
---

# Improvement Evaluator

Measures whether a Skill actually makes AI perform better on real tasks,
not just whether the SKILL.md document looks well-structured.

## Why Execution Testing Matters

Structural scoring (word count, section presence, formatting) correlates
poorly with actual AI task performance. Internal benchmarks showed R²=0.00
between document-structure scores and execution pass rates across 40+ skill
evaluations. A perfectly formatted SKILL.md can still produce failing task
outputs if the instructions mislead the model or omit critical constraints.

**Tradeoff:** Execution testing is slower and more expensive than structural
checks because it invokes the AI model once per task. A 7-task suite at
pass@1 costs roughly 7 API calls per candidate plus 7 for the baseline.
This is acceptable because structural scoring alone gives no signal about
whether the skill actually works. To offset cost, the evaluator caches
baseline results for 7 days and supports `--pass-k 1` (single attempt)
as the default to keep runs lean.

## When to Use
- Verify that a SKILL.md change improves AI task execution, not just document structure
- Run a task suite against a candidate SKILL.md and compare pass rate with baseline
- Get `execution_pass_rate` as a concrete quality metric for gating decisions
- Validate that a newly written task suite produces a sane baseline (>20% pass rate)
- Compare two versions of a skill on the same task suite to detect regressions
- Feed execution deltas into the improvement-gate for accept/reject decisions
- Debug low scores by inspecting per-task pass/fail details in the output artifact
- Run standalone evaluations during skill development without a full pipeline

## When NOT to Use
- Checking SKILL.md structure quality only (use `improvement-learner` instead)
- Scoring candidates with semantic rubrics before execution (use `improvement-discriminator`)
- Running the full generate-score-evaluate-execute-gate pipeline (use `improvement-orchestrator`)
- Measuring document formatting, section counts, or word-level metrics

## Task Suite Format

A task suite is a YAML file that defines what tasks to run and how to judge them.
Each suite targets a specific skill and contains 5-10 tasks covering the skill's
core behaviors. The schema is versioned at `"1.0"`.

```yaml
# task_suite.yaml -- minimal complete example
skill_id: "target-skill-name"
version: "1.0"
tasks:
  - id: "task-keyword-check"
    description: "Verify output mentions required concepts"
    prompt: "Given these scores {accuracy: 0.9}, what quality tier?"
    judge:
      type: "contains"
      expected: ["POWERFUL"]
    timeout_seconds: 30

  - id: "task-semantic-quality"
    description: "Rubric-scored analysis quality"
    prompt: "Accuracy dropped 0.9 to 0.8 but coverage rose. Accept?"
    judge:
      type: "llm-rubric"
      rubric: "Must mention trade-off analysis and give a recommendation"
      pass_threshold: 0.7
    timeout_seconds: 120
```

Validation rules enforced at load time:
- `skill_id` must be non-empty.
- `version` must equal `"1.0"`.
- Every task needs a unique `id`, a non-empty `prompt`, and a `judge` block.
- Judge type must be one of `contains`, `pytest`, or `llm-rubric`.
- For `contains`: `expected` must be a non-empty list of strings.
- For `pytest`: `test_file` must start with `fixtures/` (path-traversal guard).
- For `llm-rubric`: `rubric` must be non-empty.

See `references/task-format.md` and `references/writing-tasks-guide.md` for
detailed patterns and anti-patterns.

## Judge Types

The evaluator supports three judge types. Choose based on determinism needs
and output complexity.

| Judge | Mechanism | Best For |
|-------|-----------|----------|
| ContainsJudge | Checks all expected keywords appear (case-insensitive) | Deterministic presence checks, format validation |
| PytestJudge | Runs pytest on AI output via `AI_OUTPUT_FILE` env var | Structured output, JSON schema validation |
| LLMRubricJudge | LLM scores output against a rubric (0.0-1.0) | Semantic quality, open-ended evaluation |

**Because** deterministic judges (Contains, Pytest) are fast and free while
LLM judges cost an API call per evaluation, prefer deterministic judges when
the pass condition can be expressed as keyword presence or structured format.
Reserve LLMRubricJudge for tasks where semantic quality matters and no
deterministic proxy exists.

Judge configuration examples:

```yaml
# ContainsJudge -- all keywords must appear (case-insensitive)
judge:
  type: "contains"
  expected: ["validation", "sanitiz", "error handling"]

# PytestJudge -- test file receives AI output path via AI_OUTPUT_FILE
judge:
  type: "pytest"
  test_file: "fixtures/test_output_format.py"

# LLMRubricJudge -- score 0.0-1.0, pass if >= threshold
judge:
  type: "llm-rubric"
  rubric: |
    Score 0.0-1.0:
    - 0.8+: Correct analysis with actionable recommendation
    - 0.5-0.8: Partial analysis, missing specifics
    - <0.5: Generic or incorrect
  pass_threshold: 0.7
```

LLMRubricJudge supports `--mock` mode for local testing without API calls.
In mock mode the judge returns a fixed passing score so you can verify the
pipeline wiring without incurring cost.

<example>
Evaluate a candidate skill in pipeline mode:
$ python3 scripts/evaluate.py \
    --input ranking.json \
    --candidate-id c1 \
    --task-suite tasks.yaml \
    --state-root /tmp/eval-state
→ {"execution_pass_rate": 0.80, "baseline_pass_rate": 0.70, "delta": 0.10, "verdict": "pass"}
</example>

<anti-example>
Running the evaluator without a task suite file:
→ Preflight fails with "Task suite not found" -- the evaluator requires a valid task_suite.yaml.

Running with a broken task suite (baseline pass rate < 20%):
→ Aborts with verdict="error" and reason="baseline pass rate X < 0.2". Fix the suite first.
</anti-example>

## CLI Reference

Two operating modes: **pipeline mode** (with ranking artifact from discriminator)
and **standalone mode** (direct evaluation during development).

```bash
# Pipeline mode -- requires ranking artifact from discriminator stage
python3 scripts/evaluate.py \
  --input ranking-artifact.json \
  --candidate-id cand-01-docs \
  --task-suite task_suites/target-skill/task_suite.yaml \
  --state-root /tmp/eval-state \
  --pass-k 1 \
  --baseline-cache-dir /tmp/baseline-cache \
  --eval-threshold 6.0 \
  --output /tmp/eval-result.json

# Standalone mode -- evaluate a skill directly without pipeline artifacts
python3 scripts/evaluate.py \
  --standalone \
  --task-suite task_suites/deslop/task_suite.yaml \
  --skill-path ./skills/deslop \
  --state-root /tmp/eval-state \
  --mock
```

| Flag | Required | Default | Purpose |
|------|----------|---------|---------|
| `--input` | pipeline | -- | Path to ranking artifact JSON from discriminator |
| `--candidate-id` | pipeline | -- | ID of candidate to evaluate |
| `--standalone` | standalone | false | Run without ranking artifact |
| `--task-suite` | always | -- | Path to task suite YAML |
| `--state-root` | always | -- | Directory for evaluation state and output |
| `--skill-path` | standalone | -- | Path to SKILL.md or skill directory |
| `--pass-k` | no | 1 | Attempts per task (passes if any attempt succeeds) |
| `--baseline-cache-dir` | no | none | Cache baseline results (7-day TTL) |
| `--eval-threshold` | no | 6.0 | Minimum discriminator score to proceed |
| `--mock` | no | false | Use mock execution, no claude CLI needed |
| `--output` | no | auto | Override output path (default: `<state-root>/evaluations/<run-id>.json`) |

## Output Artifacts

The evaluator writes a JSON artifact to `<state-root>/evaluations/<run-id>.json`
(or the path specified by `--output`). Downstream consumers are the improvement-gate
and improvement-orchestrator.

| Field | Type | Description |
|-------|------|-------------|
| `execution_pass_rate` | float | Candidate pass rate (0.0-1.0) |
| `baseline_pass_rate` | float | Original SKILL.md pass rate (0.0-1.0) |
| `delta` | float | `candidate - baseline`; non-negative means improvement |
| `verdict` | string | `pass`, `fail`, `skipped`, or `error` |
| `candidate_results` | array | Per-task breakdown with task_id, passed, score, duration_ms |
| `baseline_results` | array | Same structure for baseline run |
| `truth_anchor` | string | Absolute path to this artifact for audit trail |

Verdict logic: `pass` when delta >= 0 (candidate is at least as good as baseline).
`skipped` when candidate discriminator score is below `--eval-threshold`.
`error` when baseline pass rate < 20% (broken task suite).

## Related Skills

- **improvement-discriminator** -- Runs semantic scoring before this stage.
  Produces the ranking artifact that this evaluator consumes. Use discriminator
  when you need LLM panel review scores, not execution-based pass rates.
- **improvement-gate** -- Consumes this evaluator's output artifact. Applies a
  6-layer mechanical gate (Schema, Compile, Lint, Regression, Review, HumanReview)
  to decide whether to accept or reject the change.
- **improvement-orchestrator** -- Coordinates the full pipeline: generate,
  discriminate, evaluate, execute, gate. Use orchestrator when you want the
  end-to-end flow rather than running individual stages.
- **improvement-learner** -- Structural quality scoring (6-dimension). Use learner
  when you only care about document quality metrics, not execution effectiveness.
