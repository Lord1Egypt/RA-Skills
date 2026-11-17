# Methodology · Hybrid

## Applicable Scenarios
When a single pure methodology is not enough: in a large system, **hardware follows waterfall while software follows agile**; or **external stage-gate compliance
plus internal agile delivery**; or **portfolio-layer waterfall roadmap + component-layer sprints**. Hybrid is not "mixing at random" but
"layering along clear boundaries".

## Three Common Forms

| Form | Macro layer | Micro layer | Governance focus |
|------|---------------|---------------|----------|
| Macro waterfall + micro agile | stage gates / roadmap | in-component Sprints | gate review + increment demos |
| Hardware waterfall + software agile | hardware serial delivery | software continuous iteration | interface/dependency alignment |
| Portfolio waterfall + component agile | portfolio roadmap | each project's chosen framework | dependencies, benefits, coordination |

## Core Artifacts (hybrid-specific templates)
- `templates/hybrid/hybrid_governance.md`: governance map—which parts use which methodology, where the gates are, who decides
- `templates/hybrid/macro_micro_map.md`: macro-micro mapping—correspondence between macro milestones ↔ micro iterations

> Other artifacts are drawn from the applied methodology: the macro layer uses waterfall/*, the micro layer uses agile/* or iteration/*.

## Operational Requirements (mandatory, see references/hybrid_playbook.md)
1. **Each macro workflow (Wave / phase) has at least 1 micro-layer plan attached**: sprint_plan / product_backlog / iteration_plan.
   The consistency check (`consistency_check.py`) will therefore block hybrid projects with no micro plan.
2. **Boundaries and gates must be explicit**: `hybrid_governance.md` states clearly which part goes macro, which goes micro, where the gates are, and who decides.
3. **Alignment review**: set an alignment review before each stage gate to verify whether the micro-layer increments meet the gate entry criteria (playbook §5).
4. **Change control**: hybrid projects must have a `change_log` + CCB (playbook §6); scope/schedule/resource changes go through the formal channel.
5. **Merged metrics dashboard**: portfolio-layer EVM (macro) + velocity/burndown (micro) merged into `portfolio_dashboard`.

## Cadence
- Macro layer: stage-gate / roadmap reviews (low frequency, heavy)
- Micro layer: Sprint / iteration cadence (high frequency, light)
- Alignment points: set an "alignment review" before each macro milestone to verify whether micro-layer increments meet gate entry.

## Key Metrics
- Portfolio layer: EVM (macro) + velocity/burndown (micro) merged dashboard (program/portfolio_dashboard)
- Dependency-blocker count (cross-layer dependencies in hybrid_governance)

## Notes
- You must **explicitly state boundaries and gates** in `hybrid_governance.md`, otherwise hybrid becomes chaotic.
- `project.yaml.methodology = hybrid`, `framework` may be empty; the governance map is a mandatory output.
- Cross-layer dependencies are the biggest source of risk—enter them into `raid.dependencies` and put them on a dependency map (program/dependency_map approach).
