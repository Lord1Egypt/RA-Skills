---
plan_id: your-plan-id
name: Your Plan Name
version: 1.0.0
description: One sentence. What this plan does and when to run it.
parameters:
  example_string:
    type: string
    required: true
    description: Description of what this controls.
  example_optional:
    type: number
    required: false
    default: 0.75
    description: Description with default noted.
  example_contact:
    type: contact_id
    required: false
    description: Weave person_id. If omitted, a random contact is selected.
steps:
  - id: step-one
    name: Step One Name
    skill: ocas-skill-name
    command: skill.command.name
    on_failure: abort
  - id: step-two
    name: Step Two Name
    skill: ocas-other-skill
    command: other.command.name
    on_failure: skip
  - id: step-three
    name: Step Three Name
    skill: ocas-third-skill
    command: third.command.name
    on_failure: abort
---

# Your Plan Name

## Purpose

One paragraph. Why this plan exists, what problem it solves, and under what conditions it should run.

---

## Step 1: step-one

**Skill:** ocas-skill-name
**Command:** skill.command.name

**Inputs:**
- `mode`: `"lookup"`
- `id`: `{{params.example_string}}`

**Outputs:**
- `record`: the full record returned by the skill -- referenced by later steps as `{{steps.step-one.record}}`

**On failure:** abort
**Notes:** Any special handling, edge cases, or execution guidance for this step.

---

## Step 2: step-two

**Skill:** ocas-other-skill
**Command:** other.command.name

**Inputs:**
- `target_name`: `{{steps.step-one.record.name}}`
- `threshold`: `{{params.example_optional}}`

**Outputs:**
- `results`: list of findings from this step
- `count`: number of items found

**On failure:** skip
**Notes:** If this step is skipped, step-three will receive `null` for any inputs derived from it and must handle that gracefully.

---

## Step 3: step-three

**Skill:** ocas-third-skill
**Command:** third.command.name

**Inputs:**
- `subject`: `{{steps.step-one.record.name}}`
- `prior_results`: `{{steps.step-two.results}}`  (may be null if step-two was skipped)
- `confidence_floor`: `{{params.example_optional}}`

**Identity heuristics** (include this block for Scout and Sift steps):
- Require: name + at least one of (email | location | employer | phone)
- Common name guard: require name + two secondary facts before accepting a match

**Outputs:**
- `enrichment_summary`: summary of what was found and written

**On failure:** abort
**Notes:** Only write facts that pass the confidence threshold. Use `source_type: inferred` with the source URL or reference as `source_ref`.
