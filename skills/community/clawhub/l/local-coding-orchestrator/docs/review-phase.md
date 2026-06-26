# Review phase

This document defines the next-stage formalization of review work in `local-coding-orchestrator`.

## Goal

Treat review as its own orchestration phase rather than as an informal afterthought.

## Review phase responsibilities

A review worker should:
- inspect the candidate outcome or probe result
- classify risks and blockers
- distinguish environment blockers from implementation blockers
- produce a concise review artifact or recommendation

## Review phase outcomes

Typical review outcomes:
- `approved-for-next-step`
- `blocked-by-environment`
- `changes-requested`
- `ready-for-hardening`

## Near-term implementation direction

The scaffold should support a lightweight review worker handoff after:
- probe completion
- implementation completion
- failed or ambiguous execution that needs triage

## Why this matters

Without a formal review phase, the supervisor is forced to infer too much from raw worker summaries.
A dedicated review phase gives the orchestrator a clearer place for judgment, classification, and handoff.
