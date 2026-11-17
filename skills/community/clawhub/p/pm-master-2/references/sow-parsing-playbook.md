# SOW / Contract Parsing Playbook (Foundation-Layout Hardening)

> **Positioning**: Parsing any "contract / letter of intent / SOW / statement of work" is the foundation layout of a program.
> If this step is done crudely (applying a generic phase, missing the commercial structure), all later scheduling, billing, and risk work will be inaccurate.
> This Playbook hardens "expert-level understanding" into a **repeatable, verifiable pipeline** that fits all contract types and all methodologies.

---

## 0. Scope of Application

- **Contract types**: fixed-fee SOW, T&M (capped-effort) contract, hybrid (fixed + milestone + T&M), letter of intent (LOI), framework agreement, subcontract.
- **Methodologies**: waterfall (stage/Wave), agile (Epic/Sprint/Release), T&M (capped-effort package), hybrid.
- **Levels**: both single project (project) and program (program, with multiple SOW sub-projects) apply.

This Playbook depends on no specific client/project; all project-specific information comes from the input **comprehension record (spec)**.

---

## 1. Reliability Loop (a + c)

To "ensure reliability," parsing takes two complementary input channels:

- **(a) Text extraction**: dump the SOW PDF text to `.txt` (or paste the original) and feed it to the parser. Read verbatim the four sections — **billing/deliverables, scope boundary, entry conditions, assumptions** — do not infer from impression.
- **(c) Guided Q&A**: when the text is ambiguous (fee currency, number of Waves, entry conditions, role ownership), the parser uses `render_ui`/direct questions to clarify with the user — **do not guess**.

The output is a structured **comprehension record (spec, JSON)**, which is then handed to `parse_sow.py` to generate the WBS. Writing to `project.yaml` is a **destructive, explicit action gated behind `--apply`**: `parse_sow.py` deletes the old SOW subtree and replaces it, only after writing a dated backup of `project.yaml`. `--dry-run` (or running with neither flag) only previews the packages. The comprehension record must pass the (a) text-extraction + (c) guided-Q&A double confirmation **before** `--apply` is issued — that double confirmation is the human checkpoint; `--apply` is the deliberate persist step, never automatic.

---

## 2. Expert-Level Comprehension Chain (CoT + Critic)

After the parser receives the text, it **must** execute the following chain-of-thought, no step-skipping:

1. **Commercial structure first**: extract verbatim events like "<Deliverable> post sign-off / completion certificate / acceptance" and their fees. Each is a candidate **billing milestone**.
2. **Scope boundary**: clarify in-scope / out-of-scope, logical vs physical, whether ETL transformation rules are included, semantic-layer ratio, special items such as archival/training.
3. **Entry conditions / data-readiness gate**: SME availability, real data, interface docs, infrastructure readiness — these are the biggest rework risk and must become explicit predecessor packages on the critical path.
4. **Assumptions are change triggers**: write "≤N source tables / M core tables / role cap" as `raid.assumptions`; exceeding the bound goes through a CCB change request.
5. **Wave / workflow decomposition**: map each billing milestone to a workflow (Wave / Phase / Epic); the workflow contains its own "analyze → design → build → map → sign-off" activities.
6. **Critic self-review** (mandatory before writing the spec, and after persisting to disk you must run `scripts/critic_review.py --strict` to pass):
   - Did you miss any billing event? (missing milestone = unmeasurable plan)
   - Does the schedule only cover the first few weeks, not all Waves? (= junior level)
   - Are all leaf packages ≤10 person-days (the **fortnight granularity**, see control.leaf_granularity)? (otherwise the control gate hard-fails)
   - Are entry conditions explicitly predecessor packages (entry_gate)?
   - The **6-factor decomposition discipline** (scope / milestone / payment / assumptions / constraints / dependencies) must all be traceable:
     every leaf must have a deliverable/scope and belong to some milestone (milestone_ref); every fixed-fee SOW has a billing milestone linked to a sow_map payment row;
     raid.assumptions must contain quantifiable bounds (≤N source tables / M core tables) so the CCB can trigger; external predecessor constraints must have an entry_gate leaf; the dependency network is connected with no orphan packages.
   - After persisting to disk, set `decomposition.critic_passed: true` (consistency_check validates this flag during planning; missing = fatal).

---

## 3. Comprehension Record (spec) Schema

`parse_sow.py --spec sow1.spec.json` accepts JSON:

```json
{
  "sow": "SOW1",
  "name": "Data Modelling & Engineering",
  "methodology": "waterfall",            // waterfall | agile | tm | hybrid
  "objective": "...",
  "scope": "...",
  "out_of_scope": "...",
  "assumptions": ["≤1600 source tables...", "..."],
  "roles": ["ba", "solution-architect", "etl-engineer", "domain-sme"],
  "entry_gates": [
    {"id": "SOW1.0", "name": "Source-Readiness Gate", "acceptance": "...", "role": "ba",
     "duration_days": 10, "estimate": 8, "dependsOn": ["SOW9"]}
  ],
  "waves": [
    {
      "id": "SOW1.W1", "name": "Wave 1 — Source Set 1",
      "billing": {"event": "Wave 1 Design Document post sign-off", "fee": 11645092,
                  "currency": "INR", "fee_type": "fixed"},
      "leaves": [
        {"id": "SOW1.W1.1", "name": "Source system identification and requirements analysis", "role": "ba",
         "duration_days": 8, "estimate": 6, "acceptance": "..."},
        {"id": "SOW1.W1.2a", "name": "Logical model FSDM", "role": "solution-architect",
         "duration_days": 8, "estimate": 6, "acceptance": "..."}
      ]
    }
  ],
  "deliverables_non_billing": [
    {"id": "SOW1.AR", "name": "Cold-data archival design",
     "billing": {"event": "Data Archival Design Document sign-off", "fee": 0, "fee_type": "none"},
     "leaves": [ {"id": "SOW1.AR.1a", "name": "...", "role": "nos-architect",
                  "duration_days": 9, "estimate": 7, "acceptance": "..."} ]}
  ]
}
```

Field rules:
- `fee_type`: `fixed` (fixed-fee, fee>0 → billing milestone) | `tm` (capped effort, package carries `billing.cap`, milestone is delivery sign-off not a fixed fee) | `none` (pure deliverable, fee=0).
- `waves[].leaves[].estimate` is required and **>0 and ≤10 person-days** (hard control-gate threshold). `duration_days` is optional (used for scheduling; default = estimate).
- When `dependsOn` is not given explicitly, the script generates the default chain: entry_gate → Wave1 → Wave1 leaf chain → W1 milestone → Wave2 …; non-billing deliverables depend on the first entry_gate, their internal leaf chain reaching the delivery milestone.
- summary / milestone packages' `estimate` is **rolled up bottom-up** by the script from children; no manual entry needed.

---

## 4. Methodology Variants

| Methodology | Workflow naming | Billing milestone source | Leaf package meaning |
|--------|-----------|---------------|-----------|
| waterfall | Wave / Phase | Design document / completion certificate sign-off | domain activities ≤10 person-days |
| agile | Epic / Release | Sprint/Release goal reached | ≤10 person-day Story/Sprint tasks |
| tm | Capped-effort package | Stage acceptance (non-fixed fee) | ≤10 person-day effort buckets, estimate within cap |
| hybrid | Wave + iteration | Fixed milestone + iteration acceptance | mixed |

`parse_sow.py` only faithfully renders the spec; the methodology decides **how the parser splits waves/leaves**, not the script logic.

---

## 5. Generation & Validation

```bash
# 1) Export a blank spec template
python3 parse_sow.py --emit-spec-template > sow1.spec.json

# 2) (parser fills the spec: from text extraction + Q&A)

# 3) Generate and persist to project.yaml (requires explicit --apply; a dated backup is written first)
python3 parse_sow.py --project program/project.yaml --spec sow1.spec.json --apply

# 4) Dry run (only print the packages to be written, do not persist)
python3 parse_sow.py --project program/project.yaml --spec sow1.spec.json --dry-run
```

Script behavior:
- **Destructive replacement is gated behind `--apply`** (see §1): `parse_sow.py` deletes the old subtree for that SOW in `project.yaml` (`id == SOWn` or `id starts with "SOWn."`), then appends new packages → **idempotent, re-runnable, and always preceded by a dated backup** (`project.yaml.bak-<date>`). With neither `--apply` nor `--dry-run` it only prints a preview and writes nothing.
- Rolls up summary/milestone estimates; default dependency chain guarantees forward scheduling.
- Writes/updates that SOW's `fee` / `fee_type` / `methodology` / `status` in `sow_map`.
- Automatically runs `consistency_check.py` at the end; if a fixed-fee SOW has no billing milestone, the consistency gate **fails fatally** (see below).

---

## 6. Foundation-Layout Consistency Gate (consistency_check hardening)

New rules (control level, fatal):
- **Billing milestone completeness**: for any SOW in `sow_map` with `fee_type: fixed`, or any child package with `billing.fee_type=='fixed' and fee>0`, the SOW subtree **must contain ≥1 package with `milestone: true` and `billing.fee_type=='fixed'`**, otherwise it is blocked.
- **Methodology consistency**: a SOW summary package's `methodology` (if provided in spec) must be compatible with `project.methodology` (when program=waterfall, sub-projects may be waterfall/agile/hybrid; swapping out of thin air is not allowed).
- Existing rules (leaf package ≤10 person-days, mandatory estimate, complete dependencies) remain in effect.

> These gates guarantee: any "foundation layout" written will **necessarily** contain billing milestones, fine-grained leaves, and complete dependencies — structurally preventing junior-level plans.

## 7. Schedule Linkage (Pillar 2 + 4)

After foundation-layout parsing, the scheduling phase must ensure "collection cadence = delivery cadence", preventing "tasks laid out but billing events not connected to the schedule".

- **Pillar 2 · Milestone↔Activity rollup**: when `parse_sow.py` generates each Wave, it automatically sets `milestone_ref: <WAVE>.M` on all its leaves (each leaf explicitly belongs to its billing milestone). `build_schedule.py` renders the "Milestone Coverage" section accordingly, listing the activities directly attributed to each milestone; one payment milestone may correspond to multiple activities.
- **Pillar 4 · Payment milestone↔schedule linkage**: `parse_sow.py` automatically sets `billing.payment_id: {SOW}-P{n}` on each billing milestone (n = 1-based index of that Wave in spec.waves). `build_schedule.py` renders the "Payment Linkage" section, mapping each fixed-fee payment row → its milestone → scheduled date vs contract `due_date`, with status:
  - `linked`: scheduled date ≤ contract due_date (consistent)
  - `drift`: scheduled date later than contract due (needs correction or a change request)
  - `no-due`: contract due_date not filled (must supply contract date)
- **Consistency gates (6d, fatal only during planning)**:
  - **6d-1 milestone coverage gap**: any leaf has neither a `milestone_ref` nor its dependency tail landing on any milestone → fatal.
  - **6d-2 payment↔milestone missing**: any fixed-fee payment row (fee>0) in `sow_map`/`program.sows` whose SOW subtree has no `milestone + billing.fee_type=fixed` package → fatal.
  - **6d-3 payment order non-monotonic**: a single SOW's billing milestone scheduled dates must be ascending (payment cadence aligned with delivery cadence) → otherwise fatal.
- During operations (already frozen, e.g. the example client), 6d is automatically skipped to avoid breaking a baselined project.
