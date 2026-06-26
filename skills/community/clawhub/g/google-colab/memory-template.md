# Memory Template - Google Colab

Create `~/google-colab/memory.md` with this structure:

```markdown
# Google Colab Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending | complete | paused | never_ask

## Activation Preferences
- When this skill should auto-activate
- When this skill should stay silent
- Proactive vs explicit-only behavior

## Runtime Context
mode: prototype | benchmark | training | teaching
runtime_policy: cpu_only | gpu_allowed | gpu_required
budget_policy: strict | moderate | flexible
reproducibility_level: baseline | strict

## Active Notebook Priorities
- Notebook objective and owner
- Exit criteria and metric target
- Current blocker

## Data Contracts
- Approved data sources
- Required schema fields
- Validation gates before long runs

## Open Risks
- Cost risk
- Data quality risk
- Reproducibility gap

## Notes
- Durable decisions and constraints
- Reliable patterns worth reusing

---
*Updated: YYYY-MM-DD*
```

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | Context still evolving | Keep refining scope and reproducibility controls |
| `complete` | Baseline workflow is stable | Focus on optimization and maintenance |
| `paused` | User paused implementation | Keep context read-only until resumed |
| `never_ask` | User wants no setup prompts | Do not ask integration questions unless requested |

## File Templates

Create `~/google-colab/notebooks.md`:

```markdown
# Notebook Registry

## Notebook Name
- Owner:
- Objective:
- Runtime class:
- Dependencies pinned:
- Exit criteria:
- Status:
```

Create `~/google-colab/experiments.md`:

```markdown
# Experiment Log

## YYYY-MM-DD - Experiment Name
- Notebook:
- Runtime and seed:
- Dataset version:
- Metrics:
- Decision:
- Next action:
```

## Key Principles

- Keep notes short, verifiable, and operational.
- Prefer explicit boundaries over broad assumptions.
- Update `last` whenever status or risk context changes.
