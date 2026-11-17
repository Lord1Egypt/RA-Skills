---
name: "kaleidosphere"
description: "Use for bounded KaleidoSphere status, discovery, analyze, plan, preview, readback, or advisory BI presentation review; reject unsafe authority."
---

# KaleidoSphere

Use this skill only for KaleidoSphere's existing closed, authority-free external contract.

## Closed capability contract

The only allowed actions are:

- `status`
- `discovery`
- `analyze`
- `plan`
- `preview`
- `readback`

Before any dispatch, validate the request with `scripts/validate-request.mjs`. Never widen the action set.

- `status`, `analyze`, and `readback` accept an empty input object only.
- `discovery` accepts only `command`, `sessionId`, optional `field`, and optional `value`. The command must be one of `start`, `resume`, `status`, `answer`, `revise`, `confirm`, or `export`.
- `plan` and `preview` accept only `objective` and optional `receiptId`.
- Refuse unknown fields, free SQL, credentials or tokens, raw source rows, arbitrary URLs, provider payloads, apply/write/delete/deploy requests, or requests that bypass preview, trusted UI approval, readback, or rollback.
- A validated request is a proposal to use an existing configured KaleidoSphere transport. It does not grant credentials, discover an endpoint, or authorize mutation.
- Attest product, contract version, capability digest, request/action binding, result integrity and freshness before accepting evidence. Treat malformed, tampered, replayed, stale, or capability-missing results as denied, with no accepted evidence.

If no trusted KaleidoSphere transport is already configured, stop after validation and return `WAITING_EXTERNAL` with the exact missing dependency. Do not accept a user-supplied arbitrary URL or secret as a workaround.

## Workflow

1. Map the request to exactly one closed action. If it cannot be mapped without widening the contract, refuse it.
2. Build the smallest closed JSON request and validate it locally.
3. State the non-claims and whether the next step is read-only, reversible discovery evidence, or proposal-only.
4. Dispatch only through an already configured trusted KaleidoSphere transport exposed by the host. Never invent a tool, endpoint, credential, or result.
5. Validate the returned attestation and evidence binding before summarizing it.
6. Keep observed facts, computed facts, inferred candidates, and human decisions separate.
7. For `plan` or `preview`, state that persistent changes still require exact trusted-UI approval, BI-Control apply, independent readback, and rollback.

## Visual review boundary

Visual guidance is advisory and never a BI truth or evidence judge.

- PanSphaira UI/HMI and other multi-step product UI: do not use taste guidance as implementation authority. At most provide an explicitly non-binding visual critique.
- Internal design review: visual hierarchy, typography, spacing, contrast, composition, and motion feedback may supplement deterministic product and accessibility evidence, never override it.
- KaleidoSphere/BI presentations: visual clarity and narrative structure may be reviewed, while all data, claims, provenance, and evidence must be verified independently.

Never infer correctness, factual truth, data quality, approval, accessibility certification, production readiness, or deployment readiness from appearance.

## Output

Return:

- action and closed request, or the precise refusal reason
- validation result
- evidence/attestation status
- observed facts, computed facts, inferred candidates, and human decisions in separate sections when present
- authority boundary and non-claims
- `WAITING_EXTERNAL` only for the specific missing configured transport or external evidence

Do not claim marketplace presence, host runtime compatibility, deployment, production readiness, or customer-data fitness without separate public evidence.
