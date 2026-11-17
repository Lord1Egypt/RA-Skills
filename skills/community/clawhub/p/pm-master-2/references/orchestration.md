# Multi-Agent Hybrid Dispatch · Orchestration Handbook

This file is PM Master's "dispatch brain". The master Agent (the PM loading this skill) uses it to decide whether to
do the work itself, form a team to run in parallel, or fork a relay.

## 1. Classification (do this first on every request)

Determine four dimensions and write them into `project.yaml` (or use them directly for routing):

| Dimension | Values | Source |
|------|------|------|
| `type` | project / program | whether the user says "project" or "program/portfolio" |
| `methodology` | waterfall / agile / iteration / hybrid | user-specified or inferred from the nature of the delivery |
| `phase` | Initiation/Planning/Execution/Monitoring/Closeout (programs also have portfolio phases) | current progress |
| `intent` | planning/building/reporting/analysis/governance | what the user wants |

## 2. Execution-Mode Decision Tree

```
Request comes in
  │
  ├─ single artifact or explanation/tweak or running one analysis  ──►  direct (master does it directly, calling render.py / evm.py etc.)
  │
  ├─ multiple "mutually independent" artifacts (e.g., initiation needs charter+WBS+schedule+risk+RACI)
  │     with no strong dependencies among them  ──►  team (TeamCreate parallel dedicated sub-Agents)
  │
  └─ needs full-context relay (e.g., "continue from last time's risk analysis", "rewrite the WBS based on the scope we just discussed")
         ──►  fork (sub-Agent inherits all context of this session)
```

**Don't form a team needlessly**: simple tasks are cheaper done directly; only form a team when artifacts are mutually independent and voluminous.

## 3. team Mode: Parallel Dedicated Sub-Agents

Use the Agent tool to dispatch multiple `general-purpose` sub-Agents **in the same message** (i.e., in parallel), each with a
self-contained brief. The master then aggregates and runs the consistency check.

### 3.1 Standard Sub-Agent Brief Template

```
You are the [<role>] dedicated sub-Agent of PM Master. Please independently produce the following PM artifact; do not reply to the user directly.

## Input
- Project source of truth: <absolute path>/project.yaml (first read it with project_state.py to understand the project background)
- Template: <absolute path>/templates/<methodology>/<template>.md
- Render engine: <absolute path>/scripts/render.py

## Task
1. Based on project.yaml and the user's requirements, organize the data needed for this artifact and write it as <slug>_data.yaml.
2. Run: python3 <SKILL_DIR>/scripts/render.py --template <template> --data <slug>_data.yaml --out <output path>
3. Write the artifact path back to artifacts.<key> in project.yaml (using project_state.py set).
4. Brief report: what files were produced, and 3 key conclusions.

## Constraints
- Only produce the artifact you are responsible for; do not touch other roles' files.
- Data must land in files; do not give text only in the conversation.
- If fields like owner/date are unknown, fill "(TBD)" and annotate; do not leave blanks that cause the consistency check to fail.
```

### 3.2 Typical Team Combinations

| Scenario | Parallel sub-Agents |
|------|--------------|
| Project initiation | planner(WBS+schedule) · risk(risk+RAID) · stakeholder(RACI+communication) |
| Agile initiation | planner(product Backlog) · risk(risk+RAID) · stakeholder(stakeholders+RACI) |
| Phase review | reporter(status report) · risk(risk update) · scheduler(schedule update) |
| Program initiation | program(portfolio charter+dashboard) · risk(portfolio risk) · dependency(dependency map) |
| **operational dual-track (P2+P3 parallel)** | **execution track** domain-expert(leaf packages/increments) · **monitoring track** monitoring-agent(control_engine periodic inspection + status report + RAID rolling + escalation flow-back) |

## 3.3 Layer 2: Domain Expert Dispatch (Expert Dispatch)

Layer 1 (PM-generalist) only produces PM governance artifacts; **technical work packages must be produced by the corresponding domain experts**, otherwise the WBS stays at
SOW-level coarse granularity. This is the true meaning of this skill's "multi-Agent"—dispatching experts by the activity's **domain/product/task**.

**Flow (planning phase):**
1. Draft the WBS as SOW-level summary packages, tagged with `domain` (e.g., `data-modelling`, `migration`, `masking`).
2. Run `python3 scripts/dispatch.py --project <project>/project.yaml` to generate the **dispatch plan**:
   it automatically flags domain activities missing a `role` tag and packages whose `estimate` exceeds the threshold and need decomposition, and specializes the recommended expert names.
3. For each package to be dispatched, send out a domain expert sub-Agent (using the `system_prompt` of the corresponding role in `references/expert-roles.md`,
   substituting `project.domain`/`product`), or route to an installed corresponding **expert** session in the **WorkBuddy Expert Center**.
4. The expert sub-Agent decomposes the package into leaf work packages (≤ `control.granularity_threshold` person-days, default 10),
   writing them back to `wbs` in `project.yaml` (ID prefix `<package ID>.x`), with deliverable/role/owner/estimate/DoD/dependencies.
5. The master re-renders `wbs.md` → runs `consistency_check.py` (new gate validates role tags + granularity) → if not passed, returns to the expert to keep decomposing.

**Role routing and specialization**: see `references/activity-expert-map.md` (activity keywords → role; domain/product → expert specialized name).
**Expert prompt library**: see `references/expert-roles.md` (13 domain roles + generic PM roles).

> An experienced team's WBS is not 10 SOW packages but hundreds of leaf packages—these come from domain experts decomposing domain by domain,
> not from a PM-generalist guessing alone. This layer 2 solidifies that discipline into the workflow and quality gates.

## 3.4 operational Dual-Track: P2 Execution Track + P3 Monitoring Track in Parallel

After entering `operational` (past the G1→2 control gate, waterfall/hybrid already `baseline.py --freeze`), **execution and monitoring are not serial
but two parallel Agent tracks both within `operational`** (see `references/lifecycle.md §5.3` and `references/phases/p2-execution.md`, `p3-monitoring.md`).
The master **dispatches both tracks simultaneously** in one TeamCreate message, so "doing" and "watching" run concurrently:

- **Track A · Execution track (P2)**: domain expert sub-Agents (`expert-roles.md` roles dispatched via `dispatch.py`) continuously produce leaf work packages/increments,
  writing `actuals` / `wbs_progress` / deliverables, going through change control (CCB).
- **Track B · Monitoring track (P3)**: a dedicated `monitoring-agent` periodically runs `control_engine.py` on the `control.cadence` cycle, producing `status_report` /
  `control_report`, rolling `risk_register` / `raid_log` / `milestone_list`, and **flowing RED escalation items back to the master**.

**Shared source of truth, zero field conflict** (this is the key to parallelism without locks):

| Track | Reads | Writes | Does not touch |
|------|----|----|------|
| Execution track | `project.yaml`, `baselines/`, plans | `wbs_progress` / `actuals` / deliverables / `raid.issues[]` (corrections) | control reports, status reports |
| Monitoring track | `baselines/`, `actuals`, `raid` | `control_report` / `status_report` / `raid.risks[]` rolling | the deliverables themselves |

**Closed loop**: the monitoring track finds a variance/RED → reports back to the master → the master routes the corrective action back to the execution track (appending work packages or changes) → the execution track updates `actuals` → the monitoring track re-checks in the next cycle.
The G2→3 soft gate (PM marks the monitoring cadence) is the explicit action to enter dual-track; the G3→4 closeout gate flips to `closed` after both tracks meet the exit criteria.

> Communication is a high-frequency activity during operational: formal notifications such as status reports/milestones/risk escalations are drafted by the `communication-agent`
> based on `communication.contacts[]` and sent through the `comm_send.py` approval gate (see `references/agents.md §8`, `scripts/comm_send.py`).

## 4. fork Mode: Context Relay

When the user asks for "continue" / "based on the previous" and similar strongly-dependent tasks, use the Agent tool with `subagent_type="fork"` to dispatch a sub-Agent;
it inherits all context of this session, suitable for deep tasks requiring long-chain reasoning (e.g., risk scenario simulation, layer-by-layer WBS decomposition).

## 5. Aggregation and Quality Gate

1. Collect each sub-Agent's report and confirm all artifact files are generated.
2. The master runs the consistency check:
   ```bash
   python3 <SKILL_DIR>/scripts/consistency_check.py --project <project>/project.yaml
   ```
3. When there are issues, hand the issue list to the corresponding sub-Agent to fix, or the master fixes directly; deliver after passing.
4. Delivery: update `project.yaml.artifacts`, render the formal document with `render_docx.py` as needed, and give the user the artifact list + metrics card.

## 6. Example (Agile Project Initiation)

User: "Use agile to help me kick off the 'Payment Refactor' project"

1. `init_project.py "Payment Refactor" --type project --methodology agile --framework scrum`
2. Classify → {project, agile, Initiation, building} → team mode
3. Dispatch in parallel in the same message:
   - planner-agent → `templates/agile/product_backlog.md`
   - risk-agent → `templates/common/risk_register.md` + `templates/common/raid_log.md`
   - stakeholder-agent → `templates/common/stakeholder_register.md` + `templates/common/raci.md`
4. Aggregate → `consistency_check.py` → render with `render_docx.py` → delivery list.
