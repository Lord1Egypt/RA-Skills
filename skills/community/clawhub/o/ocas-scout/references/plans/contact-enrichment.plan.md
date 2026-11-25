---
plan_id: contact-enrichment
name: Contact Enrichment
version: 1.0.0
description: Full research pipeline for a known contact — Scout profile research, Weave social graph update, entity Signal emission.
parameters:
  contact_name:
    type: string
    required: true
    description: Full name of the contact to research.
  contact_email:
    type: string
    required: false
    description: Known email address for identity anchoring.
  contact_employer:
    type: string
    required: false
    description: Known employer for disambiguation.
  contact_id:
    type: contact_id
    required: false
    description: Existing Weave person_id if known. If omitted, Weave is queried for a match.
steps:
  - id: weave-lookup
    name: Weave Identity Lookup
    skill: ocas-weave
    command: weave.query
    on_failure: skip
  - id: scout-research
    name: Scout Research
    skill: ocas-scout
    command: scout.research.start
    on_failure: abort
  - id: weave-update
    name: Weave Social Graph Update
    skill: ocas-weave
    command: weave.update
    on_failure: skip
---

## Step 1: weave-lookup

**Skill:** ocas-weave
**Command:** weave.query

**Inputs:**
- `name`: `{{params.contact_name}}`
- `email`: `{{params.contact_email}}`

**Outputs:**
- `person_id`: Weave person_id if a match is found, null otherwise
- `existing_profile`: existing Weave person record if found

**On failure:** skip
**Notes:** If Weave is not installed or returns no match, proceed with person_id = null. Scout will create a new entity.

---

## Step 2: scout-research

**Skill:** ocas-scout
**Command:** scout.research.start

**Inputs:**
- `name`: `{{params.contact_name}}`
- `email`: `{{params.contact_email}}`
- `employer`: `{{params.contact_employer}}`
- `weave_person_id`: `{{steps.weave-lookup.person_id}}`

**Identity heuristics:**
- Require: name + at least one of (email | employer | location)
- Common name guard: require name + two secondary facts before accepting a result

**Outputs:**
- `research_report`: path to completed research report
- `entity_signal_ids`: list of Signal IDs emitted to Elephas (via journal signal payload)

**On failure:** abort
**Notes:** Scout emits entity Signals to Elephas automatically during research.

---

## Step 3: weave-update

**Skill:** ocas-weave
**Command:** weave.update

**Inputs:**
- `person_id`: `{{steps.weave-lookup.person_id}}`
- `research_report`: `{{steps.scout-research.research_report}}`

**Outputs:**
- `updated_person_id`: final Weave person_id (existing or newly created)

**On failure:** skip
**Notes:** Updates Weave social graph with newly discovered relationships and identifiers. If person_id is null, Weave creates a new Person node.
