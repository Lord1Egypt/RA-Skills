---
name: institutional-governance
description: Use when Vietnam equity recommendations need D1-backed approvals, compliance checks, audit logging, decision journals, or approved target portfolio state transitions.
metadata: {"openclaw":{"emoji":"institution"}}
disable-model-invocation: false
---

# Institutional Governance

## Purpose

Use this skill as the institutional state and control layer. It governs Cloudflare D1 writes for portfolio action drafts, approvals, compliance checks, audit events, decision journals, and approved target portfolio state.

## Scope

- Vietnam equity portfolio governance.
- Cloudflare D1 persistence.
- Approval-gated state transitions.
- Compliance and audit logging.
- Decision journal records.

## Non-goals

- Do not place broker orders.
- Do not call broker APIs.
- Do not execute trades.
- Do not update live holdings unless the user provides explicit transaction or broker-import data.

## State Objects

- `recommendation`: analytical decision record.
- `portfolio_action_draft`: proposed portfolio change before approval.
- `approval`: explicit user decision to approve, reject, or request changes.
- `target_portfolio_state`: approved target weights after user approval.
- `audit_event`: append-only operational history.

## Required State Transition Rules

1. A recommendation may create a `portfolio_action_draft`.
2. A draft must include compliance checks before it can become `PENDING_APPROVAL`.
3. A draft with any `FAIL` compliance check must not be promoted.
4. Explicit user approval is required before creating `target_portfolio_state`.
5. Approval promotion must be idempotent.
6. Previous approved target state must be marked `SUPERSEDED` when a new state is approved.
7. Every state transition must write an `audit_event`.
8. Broker execution must remain disabled in this phase.

## Required Output

Return:

- `d1_write_intent`
- `affected_tables`
- `approval_status`
- `compliance_status`
- `state_transition`
- `audit_event_summary`
- `state_mutation_allowed`
- `broker_execution_allowed`
- `confidence`

`broker_execution_allowed` must be `false`.

## Vietnam Compliance Defaults

- Fail if target single-name weight exceeds portfolio maximum.
- Warn if sector exposure exceeds configured maximum.
- Warn if liquidity is insufficient for proposed target size.
- Fail if recommendation depends on missing critical financial statements.
- Warn if news or price data is stale.
- Fail if an action implies margin, derivatives, or broker execution.
- Warn if target state would reduce cash below the configured buffer.

## Guardrails

- Treat Cloudflare D1 as the source of truth for approved target state.
- Treat holdings as snapshots, not live broker positions, unless their source explicitly says otherwise.
- Record user approval text or channel in `approvals`.
- Never overwrite audit history.
- Never treat `target_portfolio_state` as an executable order.
