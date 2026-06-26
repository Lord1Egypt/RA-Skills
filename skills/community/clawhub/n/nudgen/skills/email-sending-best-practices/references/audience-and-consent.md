# Audience And Consent

## Core Guidance

- Send marketing email only to recipients with clear opt-in intent.
- Keep consent language specific to message type and frequency.
- Make unsubscribe and preference choices easy to find and easy to complete.
- Use list hygiene as a first-class operational workflow, not a cleanup event.

## Nudgen-Oriented Practices

- Model audience state with contact status and team context.
- Treat `active`, `unsubscribed`, and `bounced` as operational control states.
- Keep acquisition source and consent rationale available for audits.
- For CSV or bulk imports, stage and validate before broad campaign sends.

## Unsubscribe And Preferences

- Ensure unsubscribe links route to working unsubscribe endpoints.
- Prefer reversible preference updates over hard delete where policy permits.
- Confirm suppression states are respected across campaigns and lifecycle flows.

## List Hygiene Workflow

- Validate emails before import where possible.
- Remove or quarantine high-bounce and stale cohorts.
- Re-engage dormant recipients in small batches before broad sends.
- Exclude recently bounced and complaint-prone cohorts from warm-up sends.

## Practical Review Checklist

- Consent source is known for each major segment.
- Suppression behavior is tested end to end.
- Unsubscribe action updates contact status as expected.
- Audience queries align with campaign intent and message type.
