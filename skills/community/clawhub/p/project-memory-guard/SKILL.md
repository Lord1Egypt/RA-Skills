---
name: project-memory-guard
description: "Enforce project boundaries and memory writeback rules before anything enters project memory. Use before: writing notes into project memory, saving outputs/tasks/summaries, importing external messages into projects, migrating historical records. Triggered when anything attempts to write to project memory or when project boundary validation is needed."
---

# Project Memory Guard

Validate every memory write against project and writeback rules. Prevent contamination and schema drift.

## Input

Required fields:
- `raw_content` — the content attempting to enter project memory
- `candidate_project_id` — the project being written to
- `memory_type` — type of memory: note, finding, task, summary, record, etc.
- `source` — where this came from: user message, paper, tool output, etc.
- `timestamp` — ISO-8601 timestamp of when the content was created
- `confidence` — confidence score 0.0–1.0 for project assignment

## Output Schema

```
decision: "accept" | "reject" | "reroute"
destination: string | null          # project_id or "inbox" or null
normalized_record: object | null    # cleaned record if accepted/rerouted
contamination_risk: "none" | "low" | "medium" | "high"
missing_fields: string[] | null
reason: string
```

## Hard Rules

| Condition | Decision |
|-----------|----------|
| Missing `project_id` | **reject** — never enter formal project memory |
| Missing `memory_type` | **reject** — no formal writeback |
| Missing `timestamp` | **reject** — no formal writeback |
| Confidence < 0.6 | **reroute** to inbox |
| Cross-project ambiguity | **reroute** to inbox or cleanup mode |
| All fields present + high confidence | **accept** |

## Reroute Destinations

- `inbox` — unverified content waiting for manual review
- `cleanup` — ambiguous content needing disambiguation
- Specific project_id — when rerouting to a known project

## Normalization

When `decision` is `accept` or `reroute`, normalize the record:
- Strip identifying metadata not in schema
- Add `validated_at` timestamp
- Add `guard_version` = "1.0"
- Preserve original `raw_content` in `normalized_record.raw`

## Failure Handling

If uncertain about any field:
- Do not guess project_id or memory_type
- Set `decision = "reroute"` with `destination = "inbox"`
- List `missing_fields` explicitly
- Explain in `reason`

Never force acceptance when validation fails.
