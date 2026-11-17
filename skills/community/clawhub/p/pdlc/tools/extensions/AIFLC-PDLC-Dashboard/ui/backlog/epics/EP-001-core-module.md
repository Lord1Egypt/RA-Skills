# EP-001: Core Workflow Module

## Summary

| Field | Value |
|-------|-------|
| **Epic ID** | EP-001 |
| **Status** | In Progress |
| **Owner** | Product Owner |
| **Stories** | 18 total, 12 done |
| **Priority** | P1 — Critical Path |

## Description

Build the foundational workflow engine that handles item creation, assignment, status transitions, service-level tracking, and basic automation rules.

## Acceptance Criteria

- Items can be created via portal, email, and API
- Auto-assignment based on category and availability
- Service-level timers start on creation, pause on "waiting" states
- Full audit trail for all state transitions
- Sub-item and linked-item support
- Bulk operations (assign, close, escalate)

## Stories (12/18 complete)

- [x] Item data model and persistence
- [x] Create item flow (portal)
- [x] Create item flow (email parsing)
- [x] Assignment engine (round-robin + skills)
- [x] Status transition state machine
- [x] Service-level timer service
- [x] Notification on assignment
- [x] Notification on service-level warning (80%)
- [x] Item search and filtering
- [x] Item detail view
- [x] Comments and internal notes
- [x] Attachment support
- [ ] Bulk operations UI
- [ ] Linked items
- [ ] Sub-items
- [ ] Item templates
- [ ] Auto-escalation rules
- [ ] Service-level breach webhook

## Dependencies

- Auth service — resolved
- Notification service — in progress
- Search index — ready

---

*Last updated: 2026-06-15*
