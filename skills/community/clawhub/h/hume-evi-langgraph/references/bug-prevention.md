# Hume EVI + LangGraph Bug Prevention Rules

## Bug Registry (discovered 2026-02-23)

### BUG-001: Hume Events API Endpoint 404
- **Severity:** Critical
- **Node:** fetch_transcript
- **Issue:** `/chats/{id}/events` returns 404. Must use `/chat_groups/{group_id}/events`
- **Prevention:** Always verify 3rd-party API endpoints against actual docs. Test with real data, not mocks.

### BUG-002: Field Name Mismatch (camelCase vs snake_case)
- **Severity:** Critical
- **Node:** fetch_transcript
- **Issue:** Hume API returns `message_text` (snake_case), not `messageText` (camelCase)
- **Prevention:** Log raw first response and verify field names. Never assume casing conventions.

### BUG-003: Variable Scoping in Error Paths
- **Severity:** Medium
- **Node:** fetch_transcript
- **Issue:** `emotion_timeline` defined inside try/if block, undefined on failure path
- **Prevention:** Initialize all return-statement variables at top of function scope, before try/if blocks.

### BUG-004: LLM Audit Scoring Wrong Speaker
- **Severity:** Medium
- **Node:** audit_persona
- **Issue:** Full transcript passed to LLM without speaker isolation. LLM flagged Rep lines as Homeowner issues.
- **Prevention:** When LLM scores one side of a conversation, explicitly isolate that side's lines.

### BUG-005: In-Memory State Lost on Redeploy
- **Severity:** Critical
- **Node:** await_call_end (checkpointer)
- **Issue:** MemorySaver loses state when ephemeral host redeploys
- **Prevention:** Never use in-memory state stores in ephemeral deployments.

### BUG-008: Webhook Missing Expected Field
- **Severity:** Medium
- **Node:** await_call_end → webhook_handler
- **Issue:** Hume `chat_ended` webhook doesn't include `call_sid`
- **Prevention:** Never assume webhook payloads contain fields you need. Print actual payload first.

## Pre-Integration Checklist

Before integrating any external voice/webhook API with LangGraph:

- [ ] Test actual API endpoints with real data (not docs examples)
- [ ] Log raw response bodies and verify field names/casing
- [ ] Verify webhook payload schema against actual received payloads
- [ ] Initialize all variables used in return statements before try blocks
- [ ] Use external state store if deployment is ephemeral
- [ ] Map webhook IDs to graph thread IDs explicitly (don't assume correlation fields exist)
