# project.yaml Data Contract (Single Source of Truth)

`project.yaml` is PM Master's **Single Source of Truth (SSOT)**: the master Agent and all sub-Agents read and
write through it, ensuring consistent state and continuity across sessions. This file defines its **complete
field structure, required-field conventions, and initialization behavior**, as well as **how a sub-Agent should
handle an incomplete yaml**.

> See `examples/sample_project.yaml` for a complete runnable example; see `references/templates-index.md` for
> the field-key contract (data keys required for rendering).

---

## 1. Top-Level Structure (all fields)

```yaml
schema_version: 1                       # int, fixed at 1
project:
  id: pay-refactor                      # slug, unique
  name: Payment Refactor                # display name
  type: project                         # project | program
  methodology: agile                    # waterfall | agile | iteration | hybrid
  framework: scrum                      # scrum | kanban | null (null if not agile)
  phase: initiation                     # project: initiation/planning/execution/monitoring/closeout
                                        # program: program-definition/program-delivery/program-closeout
  status: planning
  lifecycle_state: planning             # planning|review|baselined|operational|closed (state machine, see lifecycle.md §5)
  baselined_on: null                    # baseline date (written by baseline.py)
  domain: payments                      # domain label, for expert dispatch specialization (optional)
  product: Payment Settlement           # product name, fallback for expert dispatch specialization (optional)
  created: 2026-08-01
  start_date: null                      # ISO, may be empty during planning
  target_end: null                      # ISO
  objectives: []                        # objective list
  scope: ''                             # scope description
  out_of_scope: ''                      # excluded scope
  sponsor: ''                           # sponsor (mandatory at quality gate)
  pm: ''                                # project manager (mandatory at quality gate)
  team: []                              # member list
governance:
  stage_gates: []                       # stage gate list (written by gate_engine.py: {gate, from_phase, to_phase, on, by, decision, lifecycle_before, lifecycle_after, criteria[]})
  communications: []                    # email-send audit (written by comm_send.py: { to[], subject, on, approved_by, backend, status })
  cadence: ''                           # review/reporting cadence
artifacts: {}                           # key -> relative project-root file path (artifact index)
artifacts_meta: {}                      # OAG drift detection: key -> { source_hash, rendered_at }
                                        # source_hash = content-hash of the data slice the deliverable depends on, written at render time by
                                        # build_subproject.py / rerender_docs.py; for manually rendered docs, write via
                                        # artifact_guard.py --stamp <key>. artifact_guard.py compares current data hash with source_hash;
                                        # mismatch == "data drift" (guardrail violation).
raid:
  risks: []                             # risks (must have owner/mitigation/5x5)
  assumptions: []
  issues: []                            # issues (must have owner/due)
  dependencies: []                      # dependencies (must have from/to)
metrics:
  evm: {}                               # { pv, bac, ev, ac } (baseline established during execution)
  burndown: []                          # agile/iteration burndown points
wbs: []                                 # work breakdown (each row must have estimate>0, role, domain; waterfall/hybrid need dependency network)
milestones: []                          # milestones (id/name/date/owner/status)
actuals: {}                             # operational actuals: { ev, ac, as_of, wbs_progress{} }
control: {}                             # operational control: { cadence, thresholds{}, recipients[] }
baseline: null                          # baseline pointer (written by baseline.py): { file, on, by }
program: null                           # only for type=program: { projects[], dependencies[], benefits[], sows[], contracts[], extracts[], sow_map[] }
                                        # sows[]: [{ sow, workstream, model, billing, fee }]  fee required (locked value or 'TBC — reason'), 'TBC' forbidden
                                        # contracts[]: [{ code, type, scope, vendor, status, sow, fee }]
communication:                          # external communication/email (data layer; policy/guardrails in skill root config.yaml)
  from: ''                              # sender for this project; empty falls back to config.email.default_from
  cadence: ''                           # periodic communication cadence (e.g. weekly)
  approval_override:                    # may only "tighten" approval, cannot loosen/disable install-period guardrails
    require_sponsor_cosign: false       # true = external email requires sponsor cosign (approver must include sponsor)
  contacts: []                          # stakeholder contact book (synced by stakeholder-agent from communication_plan.md):
                                        #   [{ name, role, org, email, phone, tz, note }]
```

---

## 2. Required Fields and Quality-Gate Constraints

`consistency_check.py` (control-level, exit 1 = blocks delivery) enforces the following:

| Field | Constraint | Phase |
|------|------|------|
| `project.pm` / `project.sponsor` | non-empty | any |
| `raid.risks[].owner` / `.mitigation` | every risk must have | any |
| `raid.risks[].likelihood/impact` | numeric 1–5; `score=likelihood×impact`; `severity` matches the color band | any |
| `raid.issues[].owner` / `.due` | every issue must have | any |
| `raid.dependencies[].from/to` | every dependency must have | any |
| `wbs[].estimate` | numeric and >0 (no `—`/empty/non-numeric) | any |
| `wbs` dependency network | waterfall/hybrid with multiple rows must form dependencies (otherwise critical path cannot be computed) | any |
| `metrics.evm.{pv,bac,ev,ac}` | EVM baseline must be established in execution/monitoring/closeout | execution/monitoring/closeout |
| `baseline.file` | waterfall/hybrid must be baselined before entering execution | execution/monitoring/closeout |
| micro-level plan | hybrid must have at least 1 sprint/backlog/iteration | any |
| `program.benefits[].owner` | every benefit must have an owner | program |

> Fill unknown fields with `(TBC)` and annotate, to avoid consistency-check failure; complete them before delivery.

---

## 3. Initialization Behavior

- **First time**: `init_project.py "<name>" --type <project|program> --methodology <...> [--framework scrum|kanban] [--domain <domain> --product <product>]`
  generates the complete skeleton (all keys from §1, default values as above) + standard directories `docs/ plans/ risks/ reports/ artifacts/`.
  If `<slug>/project.yaml` already exists it **skips** (no overwrite).
- **Sub-Agent / resumed session**: use `project_state.py` to read/write:
  `get <key>` / `set <key> <value>` / `exists` / `show` / `init <name> [--type --methodology --framework]`.
  All reads/writes land on the same `project.yaml`, ensuring continuity across Agents / sessions.

---

## 4. What a Sub-Agent Should Do With an Incomplete yaml

1. **File does not exist** → first `init_project.py` (or `project_state.py init`) to build the skeleton, then continue.
2. **Missing required fields** (e.g. `pm`/`sponsor` empty) → temporarily fill `(TBC)`, record it in the report so the master can complete it; **do not** fabricate values just to pass validation.
3. **Missing blocks like `wbs`/`artifacts`** → directly add the corresponding keys per the §1 structure (scripts are tolerant of this, e.g. `rollup_program_wbs.py` auto-creates a missing `wbs:` block).
4. **Field type mismatch** (e.g. estimate written as `"—"`) → correct to a numeric per the §2 constraints, or mark `(TBC)` and warn.
5. **Read-only, don't-edit** responsibility conflict → a sub-Agent only writes its own responsible deliverables and `artifacts.<key>`, never touching others' files; conflicts are resolved by the master during aggregation.

> Golden rule: **every deliverable writes back to the `artifacts` index + updates `project.yaml`** — never just provide text in the conversation.
