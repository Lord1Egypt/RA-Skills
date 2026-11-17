# Program Management

## What It Is
A program = a group of interrelated projects/components **managed together** to achieve common strategic benefits. Unlike a "Portfolio"
(invested by priority), a program emphasizes **dependency coordination and benefits realization**.

> Trigger: the user says "program/portfolio/manage multiple related projects together/large cross-department plan" → `init_project.py ... --type program`.

## Governance Model
- **Governance board**: sponsor + each component PM + PMO, periodic portfolio reviews.
- **Three-level view**: strategic-benefits level (program_charter / benefits_realization) → coordination level (dependency_map / portfolio_dashboard) → component level (each project self-managed).
- **Decisions**: add/terminate components, resource reallocation, cross-component dependency arbitration.

## Core Artifacts (program-specific templates)
- `templates/program/program_charter.md`: portfolio vision, goals, scope, governance, benefit targets, **contract boundaries & subcontracting (Contract/Extract/SOW)**
- `templates/program/portfolio_dashboard.md`: red/yellow/green health rollup dashboard of all components
- `templates/program/dependency_map.md`: cross-component dependencies and blockers
- `templates/program/benefits_realization.md`: benefit register, measurement definitions, realization tracking

## Contract / Extract / SOW Data Model (written to `project.yaml.program`)

Program governance must clarify the "build in-house vs outsource" boundary. Three new mapping tables:

- `program.contracts[]`: external contract summary. Fields `code / type / scope / vendor / status / sow`.
- `program.extracts[]`: Extract (carved-out outsourcable scope). Fields `id / scope / rationale / mode(build|outsource) / contract / note`.
- `program.sow_map[]`: SOW ↔ contract ↔ component mapping. Fields `sow / name / contract / component / milestone / status`.

Constraints (enforced by consistency check):
1. `sow_map[].sow` must correspond to a `tier: program` (or `summary: true`) summary package in `wbs` — otherwise contract-boundary drift.
2. An `extracts[].mode` marked `outsource` must bind a `contract` (non-empty), otherwise the Extract has no contract basis.
3. `contracts[].sow` and its `sow_map` entries must cross-reference consistently.
4. `sows[].fee` is required and must not be `(TBD)`/blank; when unlocked, write `TBC — reason`. `consistency_check.py` flags violations.

> Maintenance: when component decomposition writes back `wbs` (via `sync_wbs.py`), also `project_state.py set program.sow_map[?] ...`;
> or fill the three tables directly in the `program_charter` render data YAML and render with `render.py`.

## Difference from a Single Project (the master must remember)
| Dimension | Project | Program |
|------|------|--------|
| Goal | deliver a concrete outcome | realize strategic benefits |
| Management focus | scope/schedule/cost | dependencies/coordination/benefits |
| Artifact focus | charter/WBS/schedule/risk | portfolio charter/dashboard/dependency map/benefits |
| Risk | project level | cross-component dependency blockers, benefits shortfall |

## Key Metrics
- Component health rollup (CPI/SPI red/yellow/green)
- Dependency-blocker count
- Benefits realization rate (verified / planned)

## Two-Tier WBS Granularity Convention (Two-Tier WBS)

> Trigger: the user requires "the program-level WBS only down to each SOW milestone level, with the finest leaf packages at the component level".

- **Program WBS** = SOW summary packages (id without `.` or `summary: true`)
  **+ each SOW / P0's "phase milestone summary package"** (`milestone: true`, `tier: program`).
  **Leaf work packages are not expanded**—program reports only see milestone-level granularity.
- **Component (project) WBS** = the finest-grained **leaf work packages** (`tier: component`, `component: <slug>`),
  including domain-expert decomposition packages.

**Recommended three-level decomposition inside each SOW** (resolves the "too coarse / 4 packages × 1 role" complaint):
1. SOW summary package (`tier: program`, `summary: true`, e.g. `SOW1`)
2. Phase groups (`tier: component`, `summary: true`, e.g. `SOW1.1`–`SOW1.4`) — roll-up containers, **not** standalone SOWs (the kickoff engine only treats `tier: program` summaries as SOW-level, so phase groups will not spawn spurious kickoffs)
3. **Fortnight leaf packages** (`tier: component`, ≤10 days each, e.g. `SOW1.1.1`–`SOW1.4.2`) — each independently billable/acceptable, each assigned a **distinct domain-expert role** inferred from the contract/SOW via `role_catalog.py` (e.g. `ba` / `solution-architect` / `etl-engineer` / `domain-sme` …), governed by `acceptance` / `dependsOn` / `owner`.

Single-source-of-truth implementation (`project.yaml`):
- `scripts/rollup_program_wbs.py` aggregates leaves by phase into milestone summary packages and tags them with `tier`;
  adding `--derive-actuals` rolls up leaf actual % weighted by `estimate` into milestone actual %, written to `actuals.wbs_progress`.
- `build_wbs.py --view program|component` filters accordingly: the program view renders only `tier != component`,
  the component view renders only `tier == component` (can further filter with `--component <slug>`).
- The template `templates/waterfall/wbs.md` supports both views in a single output (table + mermaid Gantt).
- `build_schedule.py --granularity fortnight` produces a 2-week-bucketed plan (`Fortnight Plan` table + `section FNxx` Gantt) so leaf packages are tracked at fortnight granularity, not as one giant bar.

Aggregation rules (milestone summary package): `estimate` = sum of leaves; `start/end` = leaf extremes; `dependsOn` = previous phase's milestone;
`owner` inherited from the SOW summary; domain experts produce leaf packages, attributed to the corresponding component.

## Per-SOW Sub-Project (independent PM ownership)

> **Operating model (canonical, skill-level):** this is the standard bottom-up pattern. Components author their
> own plan/status/RAID/change-control; the program level is a *read-only rollup* produced by script. Full rules
> in `references/operation-model.md` (Iron Rule #11). Do **not** hand-maintain a parallel program RAID/status.

- **Create**: `init_project.py "SOW1 …" --type project --methodology waterfall --parent <program.yaml> --sow SOW1 --slug sow1`
  → creates `program/subprojects/sow1/project.yaml` (independent skeleton) and writes `program.projects[]` entry `{id, name, sow, slug, methodology, status, path}`.
- **Linkage**: child `project.yaml` carries `parent: {project: '../../project.yaml', sow: SOW1}`; cross-SOW dependencies live in each sub-project's `raid.dependencies[]` (e.g. `SOW1 → SOW2` model prerequisite).
- **Render**: `build_subproject.py --project subprojects/sow1/project.yaml` (or `--program <program.yaml> --sow SOW1`)
  → renders `risks/raid_log.md`, `risks/risk_register.md`, `reports/status_report.md` from the sub-project's single source of truth, and writes their paths back to `artifacts`.
- The program's `consistency_check.py` only flags **top-level** SOWs (`^SOW\d+$`) as orphans against `program.sow_map` — phase groups / leaf packages are intentionally excluded, so sub-project decomposition never triggers false drift warnings.

### Rollup (program = read-only aggregate of sub-projects)
After sub-projects are updated, the orchestrator refreshes the program view with the cross-file rollup:
```
python3 rollup_subprojects.py --program <program_dir>
  → reads each subprojects/<sow>/project.yaml (read-only aggregate; master not mutated)
  → per sub-project: milestone done/total + BAC/EV/AC/EAC/CPI
  → prints (or --json exports) a program-level aggregate view
python3 scripts/control_engine.py --project <program.yaml> --as-of <date>
  → program-level health dashboard (CPI/SPI, risk drift, milestone slip, RAID issues, change volume)
```
The program `actuals`, RAID, and status are **derived** — never hand-edited. To correct a program number, fix the
owning sub-project and re-run the rollup (see `references/operation-model.md` §4).

## Billing-Milestone-Driven WBS Decomposition (expert convention for SOW parsing)

> Trigger: a SOW's payment is gated on specific **deliverable sign-off / billing events** (not on elapsed time). The WBS MUST reflect the commercial wave structure, or the plan is "junior-level" and milestones won't appear.

When parsing a SOW, the comprehension step is NOT optional — apply a chain-of-thought + critic review before writing WBS:

1. **Extract the commercial structure first**: read the SOW's billing/fee section verbatim. Identify each *"<Deliverable> post sign-off"* (or equivalent) event and its fee. These become **milestone packages** (`milestone: true`) with a `billing: {event, fee_inr, currency, status}` block — they are the things to monitor and measure.
2. **Map each billing milestone to a wave / workstream** in the SOW's scope section. Model each wave as a `summary` package containing its own domain-expert leaf buckets (the leaf roles are inferred from the SOW text via `role_catalog.py`), ending in that wave's sign-off milestone.
3. **Sequence billing milestones** along the commercial cadence (sequential per-sign-off is the safe default for a single architecture team; overlap only if the SOW explicitly allows parallel source sets + SME availability for the whole project).
4. **Non-billing deliverables** (e.g. a design document with no separate fee) are still deliverable milestones, but flag `fee_inr: 0` + `note: deliverable but not a standalone billing event` so they aren't mistaken for revenue events.
5. **Every leaf package ≤ 10 person-days** (the control gate hard-fails otherwise): split logical/physical/S2T activities into ≤10-day expert buckets (e.g. `W1.2a` FSDM, `W1.2b` Customer System A, `W1.3a` Core DDL, `W1.3b` Semantic DDL). Summary/milestone packages get a rolled-up `estimate` = sum of children; milestones carry a small positive sign-off effort.
6. **Entry criteria / data-readiness gates** become explicit predecessor packages (e.g. `SOW1.0` Source-Readiness Gate) on the critical path — they are the biggest rework risk and must be visible.

Example data-lake project SOW1 example: 4 Waves of design documents modeled as billing milestones (example amounts, e.g. ₹XX.XM), scheduled in commercial-cadence order; it also includes one data-archival design-document delivery milestone (non-billable). The schedule renders an FN01→FN20 fortnightly view, with all 4 billing milestones on the critical path.

## Control Report · Schedule Detail in Columns

`control_engine.py`'s schedule control **no longer** crams "planned/actual/variance/overdue" into one long string,
but outputs a structured `schedule_table`: each work package / milestone on its own row, with separate columns for **planned% | actual% | variance% | status**.
At the program level, because baseline.wbs contains only milestone summary packages, it naturally aggregates to milestone-level detail; the component level details down to leaves.
Variances lagging beyond the threshold (`control.thresholds.schedule_slip_pct`, default 15%) are marked yellow/red, locating laggards at a glance.

## Master Dispatch Tips
- Use **team** mode for program initiation, dispatching `program-agent` (portfolio charter+dashboard), `risk-agent` (portfolio risk),
  and `dependency-agent` (dependency map) in parallel.
- The component layer can each be managed independently with this skill; `program.projects[]` records the component list and each one's methodology.
- See `references/agents.md` and `references/metrics.md` for details.
