# Report Rules

## Findings First

Put material findings before narrative summary. Order them by severity and
evidence strength.

## Severity

- `Critical`: user funds, data loss, security boundary, irreversible release, or production outage risk.
- `High`: public/operational contract is materially false or bypassable.
- `Medium`: meaningful drift, missing proof, partial implementation, or release/package mismatch.
- `Low`: stale or unclear claim with limited user impact.
- `Info`: investigated note, intentional exception, or follow-up context.

## Required Finding Fields

Each finding must include:

- id
- severity
- claim
- actual
- impact
- evidence
- proof status
- confidence
- next proof or fix step

## Unknowns

Unknowns are not failures. Keep them separate from contradicted or stale claims.
Explain what would be needed to resolve each one.
