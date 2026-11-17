# PM Master · Complete Usage Guide

> A "project + program" management skill for PMs in the tech industry. Builder-style, executable, with a
> built-in template library and multi-agent dispatch support, adapting to four methodologies:
> **waterfall / agile / iteration / hybrid**. This document is the skill's **complete user manual**.

---

## Table of Contents
1. [Quick Start](#1-quick-start)
2. [Capability Map](#2-capability-map)
3. [Core Concepts](#3-core-concepts)
4. [End-to-End Workflows (by scenario)](#4-end-to-end-workflows-by-scenario)
5. [Multi-Agent Dispatch Explained](#5-multi-agent-dispatch-explained)
6. [Template Library Overview](#6-template-library-overview)
7. [Script Quick Reference](#7-script-quick-reference)
8. [Dual-Track Output (Markdown → DOCX)](#8-dual-track-output-markdown--docx)
9. [Metric Definitions](#9-metric-definitions)
10. [Extension Guide](#10-extension-guide)
11. [FAQ](#11-faq)
12. [Full Example: Launch an Agile Project from Scratch](#12-full-example-launch-an-agile-project-from-scratch)
13. [Prompt Example Library](#13-prompt-example-library)

---

## 1. Quick Start

**Enable**: place the skill directory under your agent's `skills/` folder (in this environment it lives at
`/root/.codebuddy/skills/pm-master/`). The skill is available automatically per session, no extra install.

**Minimum viable three steps**:

```bash
# 1) Create workspace (the single source of truth project.yaml is generated here)
python3 <SKILL_DIR>/scripts/init_project.py "Payment Refactor" --type project --methodology agile --framework scrum

# 2) Produce a risk register from a template (prepare the data yaml, then render)
python3 <SKILL_DIR>/scripts/render.py \
  --template <SKILL_DIR>/templates/common/risk_register.md \
  --data risks.yaml --out /workspace/Payment Refactor/risks/risk_register.md

# 3) Export a formal Word document
python3 <SKILL_DIR>/scripts/render_docx.py /workspace/Payment Refactor/risks/risk_register.md
```

> `<SKILL_DIR>` means the skill root, i.e. the `pm-master/` folder containing `SKILL.md`.
> Natural-language triggering is simpler: just tell the agent "use agile to launch the Payment Refactor
> project" — no need to type commands by hand.

---

## 2. Capability Map

| Capability | Description | Applies to |
|------------|-------------|------------|
| Project initiation / planning | charter, stakeholders, RACI, WBS, schedule, risk, RAID | any methodology |
| Agile delivery | product backlog, sprint plan, DoD, burndown, retro | agile |
| Iteration delivery | iteration plan / backlog / review | iteration |
| Waterfall delivery | requirements spec, WBS, Gantt, stage gates, quality plan | waterfall |
| Hybrid governance | governance map, macro/micro mapping | hybrid |
| Program governance | program charter, portfolio dashboard, dependency map, benefits realization | program |
| Metric analysis | earned value EVM, schedule critical path, consistency check | analysis scenarios |
| Multi-agent parallel | team up to produce mutually independent deliverables | complex initiation / review |
| Dual-track docs | Markdown source → DOCX formal artifact | delivery / reporting |

---

## 3. Core Concepts

### 3.1 Single source of truth `project.yaml`
One `project.yaml` per project, at the project workspace root (`/workspace/<slug>/project.yaml`). The
orchestrator agent and all sub-agents read/write through it, ensuring **consistent state and cross-session
continuity**. Key fields:

```yaml
project:   { id, name, type(project|program), methodology, framework(scrum|kanban),
            phase, status, start_date, target_end, objectives[], scope, out_of_scope, sponsor, pm, team[] }
governance: { stage_gates[], cadence }
artifacts:  { charter: path, wbs: path, ... }   # deliverable file-path index
raid:       { risks[], assumptions[], issues[], dependencies[] }
metrics:    { evm: {}, burndown[] }
program:    { projects[], dependencies[], benefits[] }   # only when type=program
```

Read/write via `scripts/project_state.py`: `get <key>` / `set <key> <value>` / `show` / `exists` / `init`.

### 3.2 Four-dimension classification (decide first on every request)
| Dimension | Values |
|----------|--------|
| `type` | project / program |
| `methodology` | waterfall / agile / iteration / hybrid |
| `phase` | initiation / planning / execution / monitoring / closeout (programs have portfolio phases) |
| `intent` | plan / build / report / analyze / govern |

### 3.3 Three execution modes
| Mode | When | How |
|------|------|-----|
| **direct** | single deliverable / explanation / tweak | orchestrator directly runs scripts or templates |
| **team** | multiple independent deliverables (e.g. initiation needs charter+WBS+risk+RACI) | parallel dedicated sub-agents, then consistency check after consolidation |
| **fork** | needs full-context relay (e.g. "continue from last risk analysis") | sub-agent inherits this session's full context |

---

## 4. End-to-End Workflows (by scenario)

### Scenario A: Agile project launch (team mode, parallel)
**You say**: "Use agile (Scrum) to launch the 'Payment Refactor' project"

1. `init_project.py "Payment Refactor" --type project --methodology agile --framework scrum`
2. Classify → `{project, agile, initiation, build}` → choose **team** mode
3. In the same message, dispatch three sub-agents in parallel:
   - `planner-agent` → render `agile/product_backlog.md`
   - `risk-agent` → render `common/risk_register.md` + `common/raid_log.md`
   - `stakeholder-agent` → render `common/stakeholder_register.md` + `common/raci.md`
4. Orchestrator consolidates → run `consistency_check.py` → pass → `render_docx.py` renders
5. Deliver: deliverable list + key metrics card

### Scenario B: Waterfall project planning
**You say**: "Plan 'Core System Upgrade' with waterfall; produce WBS, schedule and stage gates"

1. `init_project.py "Core System Upgrade" --type project --methodology waterfall`
2. Route to `references/methodology-waterfall.md`
3. Render `waterfall/wbs.md` → `waterfall/schedule_gantt.md` → `waterfall/stage_gate_review.md`
4. Validate critical path and dependencies with `schedule_health.py`
5. Update `project.yaml.artifacts`

### Scenario C: Stage-gate review / status report
**You say**: "Generate this week's status report and compute EVM"

1. Prepare `metrics.yaml` (pv/ev/ac/bac)
2. `evm.py --data metrics.yaml` → outputs CPI/SPI/EAC and health flags
3. Render `common/status_report.md` (fill progress, variance, risks, help-needed items)
4. Optional: `render_docx.py` to export to stakeholders

### Scenario D: Program governance
**You say**: "Set up the 'Digital Transformation Program', with a portfolio dashboard and cross-project dependency map"

1. `init_project.py "Digital Transformation Program" --type program --methodology hybrid`
2. Route to `references/program-management.md`
3. Produce in parallel `program/program_charter.md`, `program/portfolio_dashboard.md`,
   `program/dependency_map.md`, `program/benefits_realization.md`
4. Write back `project.yaml.program.*`

---

## 5. Multi-Agent Dispatch Explained

### 5.1 Decision tree
```
request comes in
 ├─ single deliverable / explanation / tweak      ──► direct (orchestrator does it)
 ├─ multiple mutually independent deliverables    ──► team (parallel dedicated sub-agents)
 └─ needs full-context relay ("continue")         ──► fork (inherit session context)
```

### 5.2 Six dedicated sub-agent roles
| Role | Main deliverables | Writes back |
|------|------------------|-------------|
| planner-agent | WBS / product backlog / iteration plan | `artifacts.wbs` / `artifacts.backlog` |
| scheduler-agent | schedule / Gantt | schedule yaml + `schedule_health` |
| risk-agent | risk register / RAID | `raid.risks[]`, `artifacts.risk` |
| stakeholder-agent | stakeholders / RACI / communication plan | `project.sponsor/pm/team` |
| reporter-agent | status report / retro / closeout | `metrics` |
| program-agent | program charter / dashboard / dependency / benefits | `program.*` |

> Sub-agents do not reply to the user directly; they only produce files and report back to the orchestrator.
> Full brief templates are in `references/orchestration.md`.

### 5.3 Parallel team brief example (for a single sub-agent)
```
You are PM Master's [risk-agent] dedicated sub-agent. Produce the following PM deliverables independently;
do not reply to the user directly.
## Input
- Project source of truth: /workspace/Payment Refactor/project.yaml (read it first via project_state.py)
- Template: <SKILL_DIR>/templates/common/risk_register.md
- Render engine: <SKILL_DIR>/scripts/render.py
## Task
1. Based on project.yaml and requirements, organize data into risks.yaml
2. Run render.py to render to /workspace/Payment Refactor/risks/risk_register.md
3. Write the deliverable path back to project.yaml artifacts.risk
4. Briefly report: what was produced, 3 key findings
## Constraints
- Only produce deliverables you own; fill unknown fields with "(TBD)" and flag them
- Every risk must have an owner and mitigation (consistency-check mandatory item)
```

---

## 6. Template Library Overview

**35 usable templates** + 1 shared snippet `_macros.md`, organized by directory:

| Directory | Count | Templates |
|-----------|-------|-----------|
| `common/` | 16 | project_charter, stakeholder_register, raci, communication_plan, raid_log, risk_register, status_report, lessons_learned, closure_report, project_board, milestone_list, change_request, change_log, baseline_record, control_register, control_report |
| `waterfall/` | 5 | requirements_spec, wbs, schedule_gantt, stage_gate_review, quality_plan |
| `agile/` | 5 | product_backlog, sprint_plan, definition_of_done, burndown, retro |
| `iteration/` | 3 | iteration_plan, iteration_backlog, iteration_review |
| `hybrid/` | 2 | hybrid_governance, macro_micro_map |
| `program/` | 4 | program_charter, portfolio_dashboard, dependency_map, benefits_realization |

The **data-key contract** for each template is in `references/templates-index.md` (top-level YAML keys
needed for rendering; register new templates there).

---

## 7. Script Quick Reference

All scripts live in `<SKILL_DIR>/scripts/`, run with `python3`.

| Script | Purpose | Example command |
|--------|---------|-----------------|
| `init_project.py` | create workspace + project.yaml | `python3 init_project.py "Project Name" --type project --methodology agile --framework scrum [--domain <domain> --product <product>]` |
| `render.py` | template + data → Markdown | `python3 render.py --template T --data D.yaml --out O.md` |
| `render_docx.py` | Markdown → DOCX | `python3 render_docx.py O.md [--out O.docx]` |
| `evm.py` | earned value analysis | `python3 evm.py --data metrics.yaml` |
| `schedule_health.py` | critical path / dependencies / float | `python3 schedule_health.py --project <proj>/project.yaml` (or `--data schedule.yaml [--start 2025-08-01]`) |
| `consistency_check.py` | pre-delivery quality gate (control level, exit 1 = block) | `python3 consistency_check.py --project <proj>/project.yaml [--strict]` |
| `baseline.py` | freeze plan as baseline (prereq quality gate) | `python3 baseline.py --freeze --project <proj>/project.yaml`; `--status` to view |
| `control_engine.py` | operations control engine (periodic patrol vs baseline, exit 1 = RED escalation) | `python3 control_engine.py --project <proj>/project.yaml [--as-of 2026-08-12] [--json]` |
| `dispatch.py` | expert dispatch plan (audit WBS missing role / over threshold) | `python3 dispatch.py --project <proj>/project.yaml [--threshold 10] [--out dispatch_plan.md] [--json]` |
| `rollup_program_wbs.py` | program WBS two-leveling (milestone / component) | `python3 rollup_program_wbs.py <program>/project.yaml [--derive-actuals]` |
| `project_state.py` | single-source read/write | `python3 project_state.py get project.phase --file project.yaml` |
| `confidentiality_check.py` | **pre-publish** deep confidentiality scan (covers all file contents, including binaries/bytecode) | `python3 confidentiality_check.py [--pack <skill_root>]` (exit 1 = contains sensitive tokens, publishing forbidden) |

> Render engine `render.py` syntax subset: `{{ project.name }}` variables,
> `{{#each list}}…{{this.x}}…{{/each}}` loops, `{{#if a == "b"}}…{{else}}…{{/if}}` conditions.
> Jinja `{% %}`, filters, and macros are NOT supported.

---

## 8. Dual-Track Output (Markdown → DOCX)

- **Markdown is the single source of truth**: all templates render to `.md`, convenient for version
  control, diff, and post-processing.
- **DOCX is the formal deliverable**: `render_docx.py` prefers `pandoc`; if pandoc is absent it falls back
  to `python-docx` (supports headings, paragraphs, ordered/unordered lists, tables, bold). Verified.

```bash
python3 <SKILL_DIR>/scripts/render_docx.py /workspace/Payment Refactor/risks/risk_register.md
# outputs /workspace/Payment Refactor/risks/risk_register.docx
```

---

## 9. Metric Definitions

| Metric | Formula | Healthy threshold |
|--------|---------|-------------------|
| CPI cost performance | EV/AC | <0.95 = cost overrun |
| SPI schedule performance | EV/PV | <0.95 = schedule slip |
| CV / SV | EV−AC / EV−PV | negative = overrun/slip |
| EAC / ETC | BAC/CPI / EAC−AC | — |
| VAC | BAC−EAC | negative = will exceed budget |
| velocity / burndown (agile) | completed story points / remaining work | stable trend is good |

Full definitions and program/iteration metrics are in `references/metrics.md`.

---

## 10. Extension Guide

This skill is designed as an **extensible template library**; adding capabilities needs no engine or
SKILL.md change:

1. **Add a deliverable template**: drop `my_template.md` in the relevant directory (e.g. `agile/`) using
   `render.py` syntax for placeholders.
2. **Register data keys**: add a line in `references/templates-index.md` (template file / data keys / note).
3. **Add a methodology**: create `references/methodology-xxx.md` describing phases and ceremonies, add
   `templates/xxx/` for its templates, and register in the SKILL.md routing table and templates-index.
4. **Add an analysis script**: drop it in `scripts/`, reference it in the SKILL.md "Script Quick Reference"
   and the relevant reference doc.

---

## 11. FAQ

**Q1: Why does `{{ sprint.num }}` use `num` instead of `no`?**
PyYAML follows YAML 1.1, which coerces keys `no`/`yes`/`on`/`off` into booleans, making `{{ sprint.no }}`
render empty. The skill uniformly uses `num` (e.g. `sprint.num` / `iteration.num`) to avoid this; just write
the number directly on the data side.

**Q2: Why are there sometimes blank lines between table rows?**
`render.py` normalizes leading/trailing newlines on loop bodies, leaving only one newline at line ends — the
Markdown remains valid and does not affect rendering or DOCX export.

**Q3: Dependencies `deps` show as `['t1','t2']` in the Gantt?**
That's the list literal printed directly. The render engine already comma-joins list-type variables
(`t1, t2`). For finer formatting, pre-concatenate the string in the data.

**Q4: Can I export Word without pandoc?**
Yes. `render_docx.py` falls back to `python-docx` automatically (verified).

**Q5: Consistency check says "risk missing owner" — what now?**
Every risk must have `owner` and `mitigation`; `project.sponsor` / `project.pm` must also be set, or the
quality gate fails. Fill unknowns with "(TBD)" and flag them; complete before delivery.

---

## 12. Full Example: Launch an Agile Project from Scratch

```bash
SKILL_DIR=/root/.codebuddy/skills/pm-master

# ① scaffold
python3 $SKILL_DIR/scripts/init_project.py "Payment Refactor" --type project --methodology agile --framework scrum

# ② prepare data (risks.yaml excerpt)
cat > /tmp/risks.yaml <<'YAML'
project: { name: Payment Refactor, pm: Zhang San, sponsor: Li Si }
risks:
  - { id: R1, description: unstable third-party API, category: technical, likelihood: medium, impact: high,
      score: 12, owner: Wang Wu, mitigation: circuit-breaker+retry+load-test, status: monitoring }
YAML

# ③ render deliverable
python3 $SKILL_DIR/scripts/render.py \
  --template $SKILL_DIR/templates/common/risk_register.md \
  --data /tmp/risks.yaml --out /workspace/Payment Refactor/risks/risk_register.md

# ④ export Word
python3 $SKILL_DIR/scripts/render_docx.py /workspace/Payment Refactor/risks/risk_register.md

# ⑤ quality gate
python3 $SKILL_DIR/scripts/consistency_check.py --project /workspace/Payment Refactor/project.yaml
```

> The natural-language equivalent: "Use agile to launch the Payment Refactor project, identify the main
> risks and produce a risk register plus a Word version." In a real session the orchestrator auto-completes
> ①~⑤ and teams up in parallel for other deliverables as needed.

---

## 13. Prompt Example Library

Just use natural language to trigger; examples for reference:

- "Use **waterfall** to plan 'Core System Upgrade', produce **WBS, schedule, and stage-gate review**."
- "Use **agile Scrum** to launch 'Payment Refactor', build a **product backlog and risk register**."
- "Manage 'Data Platform' on a **2-week iteration** basis, generate an **iteration plan and burndown**."
- "'Autonomous Driving Program' uses **hybrid**, hardware on waterfall, software on agile, produce a
  **governance map**."
- "Set up the 'Digital Transformation Program' with a **portfolio dashboard, cross-project dependency map,
  and benefits realization plan**."
- "Compute this project's **EVM** and check whether CPI/SPI are healthy."
- "Check the schedule, **find the critical path and missing dependencies**."
- "Based on the scope we just agreed, **continue** and break the WBS down to level 3 (**fork relay**)."
- "**Export these deliverables to Word** and send to stakeholders."

---

## 14. Pre-Publish Confidentiality Scan

**Before publishing any skill package (including `templates/` `scripts/` `references/` and all examples) to a shared branch / marketplace, you must run the confidentiality scan first.** The review must cover the **content of all files**, not just file paths / file names — including binary caches (e.g. `__pycache__/*.pyc`, whose bytecode embeds `co_filename` absolute paths; scanning text only would miss them).

```bash
python3 <SKILL_DIR>/scripts/confidentiality_check.py
# scans <SKILL_DIR> by default; or specify with --pack <dir>.
# exit 0 = all clear (no HIGH-sensitive tokens); exit 1 = leak found, you must de-identify before publishing.
```

Scan scope and verdict:
- **HIGH (a hit means a leak, exit 1)**: absolute paths `/Users/` `/home/` `C:\Users` (always built in), plus any customer / vendor / personal identifiers you configure in `config.yaml` under `confidentiality.high_tokens` / `confidentiality.high_patterns`. Those are intentionally **not** hardcoded in the package, so a published skill never advertises whose data it was built around. Checked in both text and binary (byte-level).
- **Whitelist (no alert, reviewed and confirmed safe)**: de-identification placeholders `example client` / `example data-lake project` / `MPP data warehouse`; generic example role `nos-architect`; generic example emails `*@example.com`; generic example currency placeholders `example ₹ amount` / `₹XX.XM`.
- If a `.pyc` is recompiled with an embedded absolute path, the scanner catches `/Users/…` at the binary layer and blocks publishing — exactly the step missed when early reviews only scanned text. `.gitignore` already ignores `__pycache__/*.pyc`, but a directory snapshot may still carry them, so rely on this scanner before publishing.

---

_This document is provided with the PM Master skill. Skill path: `<skills>/pm-master/`, entry point `SKILL.md`._
