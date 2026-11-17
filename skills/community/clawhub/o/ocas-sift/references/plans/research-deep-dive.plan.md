---
plan_id: research-deep-dive
name: Research Deep Dive
version: 1.0.0
description: Multi-source research on a topic or entity — broad scan, depth pass, and entity extraction summary.
parameters:
  topic:
    type: string
    required: true
    description: The topic, entity, or question to research.
  depth:
    type: string
    required: false
    default: standard
    description: "Research depth: standard (2-3 sources) or deep (5+ sources)."
steps:
  - id: broad-scan
    name: Broad Scan
    skill: ocas-sift
    command: sift.research
    on_failure: abort
  - id: depth-pass
    name: Depth Pass
    skill: ocas-sift
    command: sift.research
    on_failure: skip
  - id: entity-extract
    name: Entity Extraction
    skill: ocas-sift
    command: sift.extract
    on_failure: skip
---

## Step 1: broad-scan

**Skill:** ocas-sift
**Command:** sift.research

**Inputs:**
- `query`: `{{params.topic}}`
- `mode`: broad

**Outputs:**
- `research_summary`: structured research summary
- `sources`: list of sources consulted

**On failure:** abort

---

## Step 2: depth-pass

**Skill:** ocas-sift
**Command:** sift.research

**Inputs:**
- `query`: `{{params.topic}}`
- `mode`: `{{params.depth}}`
- `prior_summary`: `{{steps.broad-scan.research_summary}}`

**Outputs:**
- `depth_summary`: enriched research summary

**On failure:** skip
**Notes:** Uses prior summary to focus the depth pass. Skips if broad scan already reached sufficient depth.

---

## Step 3: entity-extract

**Skill:** ocas-sift
**Command:** sift.extract

**Inputs:**
- `content`: `{{steps.depth-pass.depth_summary}}`

**Outputs:**
- `entity_list`: extracted entities and relationships, emitted to See references/integration-notes.md for current backend architecture.

**On failure:** skip
