---
name: log
description: >
  A privacy-first, local-first provenance protocol for agent workflows.
  Emits structured audit records for important decisions, tool calls,
  state changes, and errors, so the host environment can store, verify,
  and review them safely.
---

# LOG: Local-First Provenance Protocol

## I. Purpose
Log standardizes how an agent emits structured provenance records for
important workflow events. It does not perform persistence, encryption,
approval handling, or immutability enforcement by itself. Those controls
belong to the host environment.

Use this skill when a workflow needs:
- audit-ready activity records
- debugging traces for failures or retries
- source-aware decision summaries
- host-controlled approval gates for high-impact actions

Do not use this skill to:
- record hidden chain-of-thought
- store secrets, credentials, or tokens
- dump raw private documents, attachments, or long transcripts
- claim storage guarantees the host has not implemented

## II. Event Triggers
Emit a log entry only for important workflow events, such as:
1. tool or API execution
2. significant decision or state change
3. task completion, retry, refusal, or failure
4. high-impact action that may require host approval

Do not emit logs for every minor conversational turn.

## III. Security & Redaction Rules
All emitted records must be minimal, factual, and privacy-safe.

Rules:
- never include passwords, API keys, bearer tokens, cookies, session IDs, or secrets
- replace sensitive values with `[SECRET_REDACTED]`
- never include hidden chain-of-thought or full internal reasoning traces
- prefer summaries over raw content
- when sensitive personal data is involved, log only the category of data unless explicitly required and authorized

## IV. Approval Signaling
For a high-impact action, emit a log entry with:
- `"approval_required": true`

The host environment may use this signal to pause execution until an
approval event, user confirmation, or policy check is completed.

Log emits the signal only. The host environment decides whether to block,
continue, or reject execution.

## V. Source Provenance
When relevant, include source references that explain what the action or
decision was based on.

Examples:
- user instruction
- local file name
- tool result identifier
- API response label
- workflow state snapshot

Keep source references concise and safe. Do not include sensitive raw content.

## VI. Output Contract
When logging is required, output exactly one structured record in a fenced
`json` block prefixed by `[LOG_ENTRY]`.

## VII. Required Schema
Use this exact JSON structure:

```json
[LOG_ENTRY]
{
  "timestamp": "YYYY-MM-DDTHH:MM:SSZ",
  "event_type": "observation | decision | execution | state_change | completion | error | refusal",
  "status": "success | failed | pending | intercepted | skipped",
  "actor": "assistant | skill_name | workflow_name",
  "summary": "Concise factual description of what happened",
  "decision_basis": [
    "Key fact, constraint, or condition",
    "Key fact, constraint, or condition"
  ],
  "source_references": [
    "user_prompt",
    "local:file_a.md",
    "tool_result:search_01"
  ],
  "constraints": [
    "local_only",
    "privacy_safe",
    "approval_gate"
  ],
  "impact": "low | medium | high",
  "approval_required": false,
  "payload": {
    "action": "tool name, operation name, or null",
    "parameters_summary": "Redacted summary of relevant inputs",
    "result_summary": "Redacted summary of outputs or outcome"
  },
  "error_summary": null,
  "correlation_id": "optional task or session identifier"
}
