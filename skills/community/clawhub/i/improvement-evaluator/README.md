# improvement-evaluator

Execution-based evaluation for Skill improvement candidates. Runs predefined
task suites against a SKILL.md (candidate vs. baseline), judges each task output,
and produces an `execution_pass_rate` metric that downstream gates consume.

## Directory Structure

- `scripts/evaluate.py` -- Main CLI entry point (pipeline and standalone modes)
- `scripts/task_runner.py` -- Task execution engine; calls `claude -p` and routes to judges
- `interfaces/judges.py` -- Three judge implementations: Contains, Pytest, LLMRubric
- `task_suites/` -- Per-skill task suite YAML files (5-10 tasks each)
- `references/` -- Schema docs: `task-format.md`, `writing-tasks-guide.md`
- `tests/` -- pytest suite covering evaluator, judges, and task runner

## Quick Start

```bash
# Standalone evaluation with mock (no API calls)
python3 scripts/evaluate.py \
  --standalone \
  --task-suite task_suites/deslop/task_suite.yaml \
  --skill-path ../deslop \
  --state-root /tmp/eval-state \
  --mock
```

See `SKILL.md` for full CLI reference and judge configuration details.
