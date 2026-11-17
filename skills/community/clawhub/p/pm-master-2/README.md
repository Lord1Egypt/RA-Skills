# PM Master · Project & Program Management Skill

> A **project + program** management skill for PMs in the tech industry. Builder philosophy, executable, with a built-in template library and multi-Agent orchestration, supporting four delivery methodologies: **waterfall / agile / iteration / hybrid**.

- **Version**: 2.2.17
- **License**: MIT
- **Positioning**: Every project/program request must produce a real artifact (file); advice-only responses are prohibited.
- **Discipline additions since 2.1.0**: SOW/contract parsing pipeline, executable WBS-decomposition Critic (6-factor self-audit), domain-agnostic role catalog, Operational Artifact Guardrail (OAG), bottom-up authoring & rollup, and a penetrating pre-publish confidentiality scan.

---

## 1. What Problems It Solves

Project delivery in the tech industry often gets stuck on three things: **inconsistent methodologies** (waterfall/agile/iteration/hybrid mixed arbitrarily), **no standard deliverables** (charter/WBS/risk/status reports each done their own way), and **unsustainable governance** (plans disconnected from execution, missing baselines, no periodic inspection). PM Master turns these three problems into a **executable engineering system**:

- Every request → a real file (Markdown, exportable to DOCX);
- Every project → a single source of truth `project.yaml`, continuous across sessions/Agents;
- Every discipline → a verifiable quality gate (consistency gate, baselining, operational control).

---

## 2. Core Capabilities

| Capability | Description | Applies To |
|------|------|------|
| Project Initiation / Planning | Charter, stakeholders, RACI, WBS, schedule, risk, RAID | Any methodology |
| Agile Delivery | Product Backlog, Sprint Plan, DoD, burndown, retrospective | agile |
| Iteration Delivery | Iteration Plan / Backlog / Review | iteration |
| Waterfall Delivery | Requirements Spec, WBS, Gantt, stage gates, quality plan | waterfall |
| Hybrid Governance | Governance map, macro-micro mapping | hybrid |
| Program Governance | Portfolio charter, portfolio dashboard, dependency map, benefits realization | program |
| Metrics Analysis | Earned value (EVM), schedule critical path, consistency check | Analysis scenarios |
| Multi-Agent Parallelism | Team up to produce mutually independent artifacts | Complex initiation / review |
| Dual-track Docs | Markdown source → DOCX formal document | Delivery / reporting |
| Phased Delivery | P0+P1 initiation & planning / P2 execution / P3 monitoring / P4 closeout phase modules; each phase defines activities/deliverables/criteria | Full lifecycle |
| Stage Gate Approval | `gate_engine` evaluates entry criteria + hard gates (execution/closeout) enforce approval, flipping the state machine | Phase transitions |
| Operational Dual-track Parallel | P2 execution track (domain experts) + P3 monitoring track (`monitoring-agent`) multi-Agent parallel, sharing the source of truth with zero field conflicts | Execution/Monitoring |
| External Communication & Email Approval | `communication_plan` registers the stakeholder contact book; `communication-agent` drafts, `comm_send.py` enforces an approval gate + audit, with layered configuration (install-time guardrails / project-time data) | Communication/Email |
| SOW / Contract Parsing Pipeline | `parse_sow.py` turns a confirmed understanding-record (spec) into WBS packages (idempotent, bottom-up estimate rollup, auto dependency chain, billing-milestone mapping), driven by the `sow-parsing-playbook.md` two-channel (text extract + guided Q&A) method | Initiation / SOW-driven |
| WBS Decomposition Discipline (Critic) | `critic_review.py` — executable 6-factor self-audit (scope traceable / milestone attribution / payment linkage / quantifiable assumption bounds / constraints gated / dependency connectivity); fatal in planning, advisory once baselined | Planning / WBS |
| Domain-agnostic Role Catalog | `role_catalog.py` single source for 10 technical domains + cross-domain roles; `infer_domain` / `infer_role` / `align_from_sow` — removes data-domain default bias | Any decomposition |
| Operational Artifact Guardrail (OAG) | `artifact_guard.py` content-hash drift detection — any `project.yaml` change in `operational`/`monitoring` must re-render its deliverable(s); drift = RED escalation + closeout block (Iron Rule #12) | Execution/Monitoring |
| Bottom-up Authoring & Rollup | Plans/status/RAID/change-control authored at the lowest owning unit (sub-project/SOW); program level is a read-only scripted rollup (`rollup_subprojects.py` / `rollup_program_wbs.py`) — never hand-edited (Iron Rule #11) | Program governance |
| Pre-publish Confidentiality Scan | `confidentiality_check.py` penetrating scan of the whole pack (text line-match + **byte-level** for binaries/`.pyc`), HIGH-token blocklist + reviewed-safe whitelist; mandatory before pushing to a shared branch | Release / OpSec |

---

## 3. Quick Start

### 3.1 Installation
Place the skill directory under CodeBuddy's `skills/`:

```bash
# for example
cp -r pm-master <SKILLS_DIR>/pm-master   # <SKILLS_DIR> = your agent's skills directory (e.g. ~/.codebuddy/skills)
```

The skill is automatically available per session, no extra installation needed. You can also extract the distributed `pm-master.zip` directly into that directory.

> **Install-time configuration (policy/guardrails)**: The skill root `config.yaml` defines email capability and security guardrails — `email.enabled` / `email.backend` (agent-mail·himalaya·gog·smtp) / `email.default_from` / `email.requires_send_approval` (hard guardrail, cannot be disabled at project level). Fill in as needed during install; project-level data (contact book/cadence) lives in the `communication:` block of `project.yaml`. See `references/project-schema.md` and `scripts/comm_send.py` for details.

### 3.2 Minimal Three-Step Workflow (Command Line)

```bash
SKILL_DIR=<SKILLS_DIR>/pm-master   # <SKILLS_DIR> = your agent's skills directory (e.g. ~/.codebuddy/skills)

# 1) Build the workspace (the single source of truth project.yaml is generated here)
python3 $SKILL_DIR/scripts/init_project.py "Payment Refactor" --type project --methodology agile --framework scrum

# 2) Produce a risk register from a template (prepare the data yaml first, then render)
python3 $SKILL_DIR/scripts/render.py \
  --template $SKILL_DIR/templates/common/risk_register.md \
  --data risks.yaml --out /workspace/Payment Refactor/risks/risk_register.md

# 3) Export a formal Word document
python3 $SKILL_DIR/scripts/render_docx.py /workspace/Payment Refactor/risks/risk_register.md
```

> Natural-language triggers are simpler: just tell the Agent "Use agile to help me initiate the payment refactor project" — no need to type commands manually.

> **Activation scope (bounded)**: activate only on **explicit intent to create, plan, execute, monitor, close, or govern** a project/program and its artifacts. Examples that SHOULD activate:
> - "Initiate the payment refactor project (agile)"
> - "Build the WBS for SOW1 and run the consistency gate"
> - "Run the stage-gate review to move into execution"
> - "Produce the risk register / RAID log for this program"
>
> **Negative examples (do NOT activate this skill)**:
> - "What is a Gantt chart?" / "Explain agile vs waterfall" (general PM theory, not a task on a project)
> - "Summarize this meeting note" (generic writing/summarization)
> - "Help me write a status-update email" (general composition, not the PM workflow)
> - "Plan my vacation / organize my photos" (unrelated planning language)

---

## 4. Core Concepts

### 4.1 Single Source of Truth `project.yaml`
One `project.yaml` per project/program (located at the workspace root `/workspace/<slug>/project.yaml`). The controller and all sub-Agents read and write through it, ensuring consistent state and continuity across sessions. For the full field structure see [`references/project-schema.md`](references/project-schema.md); for an example see `examples/sample_project.yaml`.

### 4.2 Four-Dimension Classification (decide per request first)
| Dimension | Values |
|------|------|
| `type` | project / program |
| `methodology` | waterfall / agile / iteration / hybrid |
| `phase` | Initiation / Planning / Execution / Monitoring / Closeout (programs additionally have portfolio phases) |
| `intent` | Planning / Build / Report / Analysis / Governance |

### 4.3 Three Execution Modes (Hybrid Orchestration)
| Mode | When to use | Approach |
|------|--------|------|
| **direct (do it yourself)** | Single artifact / explanation / fine-tuning | The controller directly calls scripts or templates to complete it |
| **team (parallel teaming)** | Multiple independent artifacts (e.g., initiation needs charter+WBS+risk+RACI) | Dispatch dedicated sub-Agents in parallel within the same message, then aggregate + consistency check |
| **fork (continue context)** | Needs full-context handoff (e.g., "continue from last risk analysis") | Sub-Agent inherits the entire context of this session |

> **TeamCreate** is this environment's multi-Agent concurrent dispatch mechanism (the team mode of the Agent tool). For sub-Agent roles and brief templates see [`references/agents.md`](references/agents.md); for the orchestration decision tree see [`references/orchestration.md`](references/orchestration.md).

### 4.4 Mandatory State Machine: Plan → Baseline → Operational Control
The mandatory serial discipline of `lifecycle_state` (see [`references/lifecycle.md`](references/lifecycle.md) §5):

```
planning → review → baselined → operational → closed
```

- **waterfall / hybrid** **must** run `baseline.py --freeze` (freeze the plan as baseline) before entering execution/monitoring;
- Only after a control gate sets `lifecycle_state` to `operational` can `control_engine.py` be used for periodic inspection;
- Projects that are not baselined (missing `baseline` pointer) **may not** enter the operational phase; the consistency gate will block directly.

### 4.5 Phase Modules & Stage Gates (Phase Modules & Gates)
Initiation→Planning→Execution→Monitoring→Closeout is split into 4 phase modules (`references/phases/`), each defining the phase's **activities / mandatory deliverables / entry criteria / exit criteria / stage-gate approval checklist**, adapted per methodology. Transitions between phases are governed by `gate_engine.py` (hard gates reuse `consistency_check` / `control_engine`; if not passed, exits 1 and refuses to proceed):

- G0→1 Initiation→Planning (soft gate / PM)
- **G1→2 Planning→Execution (hard gate / sponsor)**: requires `consistency_check.py` exit 0 (waterfall/hybrid additionally require `baseline.py --freeze`)
- G2→3 Execution→Monitoring (soft gate / PM, parallel within operational)
- **G3→4 Monitoring→Closeout (hard gate / sponsor)**: requires `control_engine.py` exit 0 + acceptance/retrospective deliverables + (program) benefits closure

See `lifecycle.md` §6 and `references/phases/*` for details.

---

## 5. Standard Workflow (follow every time)

- **Step 0 · Locate the source of truth**: Find `project.yaml`; if it doesn't exist → `init_project.py` builds the skeleton.
- **Step 1 · Classify & route**: Determine the four dimensions type / methodology / phase / intent; once `phase` is determined, read the corresponding phase module (`references/phases/*`) and proceed per its activities/deliverables/criteria; transitions between phases must pass `gate_engine.py` stage gates.
- **Step 2 · Read the methodology manual**: Per methodology read `references/methodology-*.md` (for programs read `program-management.md`).
- **Step 2.5 · Expert dispatch (break WBS down to leaf packages)**: `planner-agent` produces SOW-level summary packages; `dispatch.py` audits and generates the dispatch plan; domain-expert sub-Agents break packages down to leaf level (≤ `control.granularity_threshold` person-days, default 10).
- **Step 3 · Choose execution mode**: direct / team / fork (see §4.3).
- **Step 4 · Build artifacts**: scaffolding + `render.py` rendering + **mandatory analysis scripts** (`schedule_health` / `evm`) + **must pass `consistency_check.py`** before delivery.
- **Step 5 · Team up (team mode only)**: TeamCreate dispatches dedicated sub-Agents; the controller aggregates + consistency check.
- **Step 6 · Deliver**: Update the `artifacts` index; run `render_docx.py` as needed; summarize the artifact list + metrics card for the user.

---

## 6. Template Library (37 templates + `_macros.md`)

| Directory | Count | Templates |
|------|------|------|
| `common/` | 17 | project_charter, stakeholder_register, raci, communication_plan, raid_log, risk_register, status_report, lessons_learned, closure_report, project_board, milestone_list, change_request, change_log, baseline_record, control_register, control_report, sow_kickoff |
| `waterfall/` | 5 | requirements_spec, wbs, schedule_gantt, stage_gate_review, quality_plan |
| `agile/` | 5 | product_backlog, sprint_plan, definition_of_done, burndown, retro |
| `iteration/` | 3 | iteration_plan, iteration_backlog, iteration_review |
| `hybrid/` | 2 | hybrid_governance, macro_micro_map |
| `program/` | 4 | program_charter, portfolio_dashboard, dependency_map, benefits_realization |

The **data-key contract** for each template is in [`references/templates-index.md`](references/templates-index.md).

---

## 7. Script Quick Reference

All 28 scripts are under `scripts/`, run with `python3`. Grouped by function.

**Source of truth & scaffolding**
| Script | Purpose | Example Command |
|------|------|----------|
| `init_project.py` | Build workspace + project.yaml (project or program; program adds `--parent`/`--sow`/`--slug` for per-SOW sub-projects) | `python3 init_project.py "Project name" --type project --methodology agile --framework scrum [--domain <domain> --product <product>]` |
| `project_state.py` | Single source of truth read/write; `migrate` (v1.x→v2 schema) / `checkpoint` (anti-skip); backup-on-overwrite guard | `python3 project_state.py get project.phase --file project.yaml` |
| `role_catalog.py` | Domain-agnostic role catalog (10 tech domains + cross-domain); `infer_domain` / `infer_role` / `align_from_sow` | imported by dispatch/consistency; `python3 role_catalog.py` to inspect |

**Rendering & export**
| Script | Purpose | Example Command |
|------|------|----------|
| `render.py` | Template + data → Markdown (mini engine; helpers `sev_cell`/`assume_text`/`eq`) | `python3 render.py --template T --data D.yaml --out O.md` |
| `render_docx.py` | Markdown → DOCX | `python3 render_docx.py O.md [--out O.docx]` |
| `rerender_docs.py` | Pure-function re-render from `project.yaml` (wbs / risk_register / program_charter / change_log / raid_log / evm_report / baseline_record / control_register) — kills content drift | `python3 rerender_docs.py --project <project>/project.yaml [--only raid_log]` |

**SOW parsing & WBS decomposition**
| Script | Purpose | Example Command |
|------|------|----------|
| `parse_sow.py` | Understanding-record (spec) → WBS packages (idempotent, bottom-up estimate, dependency chain, `milestone_ref`/billing mapping) | `python3 parse_sow.py --project <project>/project.yaml --spec spec.json` |
| `dispatch.py` | Expert dispatch plan (audits WBS for missing role / over-threshold; marks satisfied packages `done`) | `python3 dispatch.py --project <project>/project.yaml [--threshold 10] [--out dispatch_plan.md] [--json]` |
| `critic_review.py` | Executable WBS Critic — 6-factor decomposition self-audit (fatal in planning, advisory once baselined) | `python3 critic_review.py --project <project>/project.yaml [--strict]` |
| `sync_wbs.py` | Merge an expert decomposition-patch YAML back into `project.yaml.wbs` (auto parent/child, validates leaf required fields) | `python3 sync_wbs.py --project <project>/project.yaml --patch decomp.yaml` |
| `build_wbs.py` | Render WBS (decomposition tree `graph TD` + optional dated gantt) from the source of truth | `python3 build_wbs.py --project <project>/project.yaml` |

**Scheduling & analysis**
| Script | Purpose | Example Command |
|------|------|----------|
| `build_schedule.py` | Forward-schedule WBS → schedule/gantt (fortnight granularity, milestone coverage, payment linkage; `--level program` / `--sow` are read-only views) | `python3 build_schedule.py --project <project>/project.yaml [--granularity fortnight]` |
| `build_sow_kickoff.py` | Per-SOW kickoff artifact (program-level SOW packages only) | `python3 build_sow_kickoff.py --project <program>/project.yaml` |
| `schedule_health.py` | Critical path / dependencies / float | `python3 schedule_health.py --project <project>/project.yaml` (or `--data schedule.yaml [--start 2025-08-01]`) |
| `evm.py` | Earned value analysis | `python3 evm.py --data metrics.yaml` |

**Quality gates & lifecycle**
| Script | Purpose | Example Command |
|------|------|----------|
| `consistency_check.py` | Pre-delivery quality gate (control level, exit 1 = blocker; integrates critic + billing-milestone + schedule-linkage gates, planning-fatal only) | `python3 consistency_check.py --project <project>/project.yaml [--strict]` |
| `baseline.py` | Freeze plan as baseline (prerequisite quality gate) | `python3 baseline.py --freeze --project <project>/project.yaml`; `--status` to view status |
| `gate_engine.py` | Stage gate engine (evaluate/approve entry into target phase; hard gates reuse consistency/control) | `python3 gate_engine.py --project <project>/project.yaml --to Execution [--approve "Zhang San(sponsor)"]`; `--status` shows current state and available gates |
| `test_gate_engine.py` | Stage gate engine unit-test suite (CI gate, 66 assertions × 4 methodologies × soft/hard/rejected/dry-run/--status) | `python3 test_gate_engine.py` (exit 0 = all pass) |
| `confidentiality_check.py` | Penetrating pre-publish scan (text line-match + byte-level for `.pyc`/binaries); HIGH-token blocklist + reviewed whitelist; **mandatory before pushing to a shared branch** | `python3 confidentiality_check.py` (exit 0 = clean) |

**Execution, control & communication**
| Script | Purpose | Example Command |
|------|------|----------|
| `execution_driver.py` | Execution driver — reads WBS state, generates the executable work-package list, tracks sprint/iteration, auto-triggers control inspection | `python3 execution_driver.py --project <project>/project.yaml [--json]` |
| `control_engine.py` | Operational control engine (periodic inspection against baseline; unified status normalization; skips summary/cancelled; OAG built-in; exit 1 = RED escalation) | `python3 control_engine.py --project <project>/project.yaml [--as-of 2026-08-12] [--json]` |
| `artifact_guard.py` | OAG content-hash drift detection (`--stamp <key>` records hash for manual/external renders) | `python3 artifact_guard.py --project <project>/project.yaml` |
| `comm_send.py` | External email approval gate (resolves recipients by role, requires `--approve`, writes `governance.communications` audit; `--dry-run` reviews only) | `python3 comm_send.py --project <project>/project.yaml --to "sponsor,pm" --subject "Milestone achieved" --body-file draft.md --approve "Zhang San(PM)"` |
| `subagent_check.py` | Validate each sub-agent JSON report against the protocol contract (Iron Rule #10) | `python3 subagent_check.py --report report.json` |

**Program rollup**
| Script | Purpose | Example Command |
|------|------|----------|
| `rollup_program_wbs.py` | Single-file two-level rollup (program = milestone level, component = leaf level; cancelled-status propagation) | `python3 rollup_program_wbs.py <program>/project.yaml [--derive-actuals]` |
| `rollup_subprojects.py` | Cross-file rollup of per-SOW sub-projects into the program view (read-only aggregate; `eac_vs_bac_var` None-guarded) | `python3 rollup_subprojects.py --program <program_dir> [--json]` |
| `build_subproject.py` | Render a sub-project's RAID / risk register / status report from its own `project.yaml` | `python3 build_subproject.py --project subprojects/<slug>/project.yaml` |

> ⚠️ **Script exception handling**: If a script is missing / path is wrong / arguments are invalid, do not fail silently — give a specific error, and degrade to: ① use `project_state.py` to maintain `project.yaml`; ② use `render.py` to render templates directly; ③ if PyYAML is missing, first run `pip install pyyaml`.

---

## 8. Key Rules (Summary)

- **Never advice-only**: Every request must produce a file or run analysis; at minimum update `project.yaml`.
- **Source of truth first**: If there's no `project.yaml`, run `init_project.py` first.
- **Use the right methodology**: agile uses backlog/sprint/burndown, waterfall uses WBS/Gantt/stage gates.
- **Estimation mandatory**: Every WBS / backlog row must have a numeric estimate (>0); placeholders are not allowed.
- **Expert dispatch + leaf-package granularity**: Technical-domain work packages must be broken down by the corresponding domain expert, tagged with `role` and `domain`, with leaf packages ≤ threshold.
- **Analysis mandatory**: Run `schedule_health` before delivering waterfall / hybrid; run `evm` during execution/monitoring.
- **Pass the quality gate before delivery**: `consistency_check.py` must exit 0 to pass; fatal items (missing estimate / schedule not networked / missing EVM baseline / hybrid missing micro-plan / risk not calibrated 5×5 / benefit missing owner / not baselined) are blocked directly.
- **Planning ≠ operationalization (mandatory serial)**: First plan → review → `baseline.py --freeze` → control gate → only then enter execution/monitoring.
- **Operational control loop**: After entering `operational`, run `control_engine.py` periodically per `control.cadence` to inspect against the baseline; RED escalation exits with code 1 and can be wired to a scheduled alert.
- **Phase transitions must pass stage gates (mandatory)**: Initiation→Planning→Execution→Monitoring→Closeout advances serially per the state machine; entering `Execution` (G1→2) and `Closeout` (G3→4) are **hard gates** that require `gate_engine.py` evaluation with all automated criteria passing and sponsor approval before flipping `lifecycle_state`; `Monitoring` (G2→3) is a **soft gate** (PM approval). Hard gates cannot be skipped (see `references/phases/*`, `lifecycle.md` §6).
- **Bottom-up authoring & rollup (Iron Rule #11)**: Plans / status / RAID / change-control are authored at the lowest owning unit (sub-project / SOW). The program level is a **read-only scripted rollup** (`rollup_subprojects.py` cross-file, `rollup_program_wbs.py` single-file two-level) — never a hand-edited parallel source. To correct a program figure, fix the source sub-project and re-run the rollup. Violation → governance drift, false status.
- **Every operational action must refresh its artifacts — OAG (Iron Rule #12)**: In `operational` / `monitoring`, any change to `project.yaml` (status / EVM / RAID / WBS / actuals) MUST re-render the dependent deliverable(s) and pass `artifact_guard.py` (exit 0). Stale/missing deliverables are a guardrail breach — flagged RED by `control_engine.py` and blocked at closeout by `gate_engine.py`.
- **Confidentiality gate before shared-branch publish**: Run `confidentiality_check.py` (exit 0) before pushing the pack to a shared branch — it scans all files (including byte-level for `.pyc`) for client/vendor names, absolute paths, and other sensitive tokens.

---

## 9. Extension Guide (no engine changes needed)

1. **Add an artifact template**: Place `my_template.md` in the relevant directory (use `render.py` syntax for placeholders).
2. **Register data keys**: Add a line in `references/templates-index.md` (template file / data key / description).
3. **Add a methodology**: Create `references/methodology-xxx.md` + `templates/xxx/`, and register them in the SKILL.md routing table and templates-index.
4. **Add an analysis script**: Place it in `scripts/`, and reference it in the SKILL.md script quick-reference and the corresponding reference.

---

## 10. Program-Specific

- Use `init_project.py --type program` to build the portfolio-level workspace.
- Portfolio charter / portfolio dashboard / cross-project dependency map / benefits realization plan are all program-specific templates.
- `rollup_program_wbs.py` two-levels the single-source `wbs`: program level = milestone level, component level = leaf work-package level; component/phase mapping preferentially reads `program.components` / `governance.waves` from `project.yaml`, falling back to built-in examples by default.
- Program phases (Portfolio Definition/Delivery/Closeout) and the lifecycle state machine (planning→…→closed) are two orthogonal layers; see `lifecycle.md` §5.3 for details.

---

## 11. Reference Index

| File | When to read |
|------|--------|
| `references/orchestration.md` | Multi-Agent orchestration, deciding execution mode |
| `references/agents.md` | Dispatch dedicated sub-Agents, write briefs |
| `references/subagent-protocol.md` | Sub-agent JSON report contract (validated by `subagent_check.py`) |
| `references/operation-model.md` | Bottom-up authoring & read-only rollup operating model (Iron Rule #11) |
| `references/sow-parsing-playbook.md` | Methodology/contract-agnostic SOW parsing (text + guided Q&A → spec → WBS) |
| `references/expert-roles.md` | Domain expert role catalog + system prompt |
| `references/activity-expert-map.md` | Activity→role routing, expert specialization, leaf-package granularity |
| `references/lifecycle.md` | Phase-deliverable matrix, lifecycle and state machine |
| `references/methodology-*.md` | Each methodology (waterfall/agile/iteration/hybrid) |
| `references/hybrid_playbook.md` | Hybrid practice: cadence/micro-plan/alignment review/change control |
| `references/risk-matrix.md` | Risk 5×5 calibration scale and color bands |
| `references/program-management.md` | Program (portfolio) management |
| `references/metrics.md` | EVM / burndown / health metric definitions |
| `references/project-schema.md` | `project.yaml` full field structure and collaboration conventions |
| `references/templates-index.md` | Full template library list and data-key contract |
| `references/usage.md` | Full usage manual (end-to-end examples, prompt library) |
| `references/phases/p0-p1-initiation-planning.md` | P0+P1 initiation & planning phase module |
| `references/phases/p2-execution.md` | P2 execution phase module |
| `references/phases/p3-monitoring.md` | P3 monitoring phase module |
| `references/phases/p4-closeout.md` | P4 closeout phase module |

---

## 12. Version & Changes

Full changelog history is in [`CHANGELOG.md`](CHANGELOG.md). Current version **2.2.17**.

**v2.1.x → v2.2.x arc (highlights):**
- **v2.1.0** — Merged refactor: v1.3.6 enforced framework + v2 architecture; restored expert-dispatch workflow (Step 2.5); wired the sub-agent protocol (`subagent_check.py`), execution driver, and config knobs; unified single English package (`SKILL.md`).
- **v2.1.1–2.1.8** — Production hardening from live use: `sync_wbs.py` decomposition write-back, WBS decomposition-tree mermaid, program-charter contract/SOW coverage, drift-proof `rerender_docs.py`, `project_state.py` data-loss guard (backup-on-overwrite), severity color icons, and multiple mermaid `&`/invalid-date fixes.
- **v2.2.0–2.2.6** — SOW/contract parsing pipeline (`sow-parsing-playbook.md` + `parse_sow.py`), billing-milestone integrity gate, WBS→schedule engine (`build_schedule.py` fortnight/coverage/payment-linkage), and scheduling-engine fixes (dependency chains, summary-package zero-duration).
- **v2.2.2–2.2.4** — Operating model (`operation-model.md`) with Iron Rule #11 (bottom-up authoring & rollup); P0/P1 method-agnostic skeleton; WBS decomposition discipline Pillar 1 (`critic_review.py` 6-factor self-audit) + Pillar 3 (fortnight granularity).
- **v2.2.9–2.2.10** — Operational Artifact Guardrail (Iron Rule #12, `artifact_guard.py` content-hash drift) integrated into control/gate engines; RAID rendering fixes (`assume_text` helper).
- **v2.2.11** — Penetrating pre-publish confidentiality scan (`confidentiality_check.py`, byte-level for `.pyc`); mandatory before shared-branch publish.
- **v2.2.12** — Domain-agnostic role catalog (`role_catalog.py`, 10 tech domains) — removed data-domain default bias.
- **v2.2.13** — Control-engine robustness (unified status normalization, skip summary/cancelled packages, terminal-lifecycle GREEN) + expanded re-render coverage (change_log / raid_log / evm_report / baseline_record) + rollup None-guards.

> **Doc sync rule**: Every skill change must keep `README.md`, `SKILL.md`, `CHANGELOG.md`, `_user_meta.json`, and the version number consistent, and must pass `confidentiality_check.py` (exit 0) before publishing to a shared branch. This OpenClaw (ClawHub) edition ships a **single English `SKILL.md`** (`SKILL.en.md` was removed in the v2.2.16 English-only unification); `README.md` is the single English reference.

_PM Master · Making project management truly "executable."_
