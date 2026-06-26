---
name: payment-incident-responder
description: Coordinate payment incident response with structured triage, blast-radius assessment, mitigation actions, stakeholder communication, reconciliation recovery, and postmortem tracking.
metadata: {"openclaw":{"emoji":"🚨","homepage":"https://www.rbi.org.in/scripts/BS_ViewMasDirections.aspx?id=12898"}}
---

# Payment Incident Responder

## Purpose

Help teams respond to payment incidents quickly and consistently:

- detect and classify incident severity
- define immediate containment actions
- coordinate internal/external communication
- restore correctness via reconciliation and data repair
- produce postmortem action items

## Disclaimer

This skill provides operational guidance only. It does not execute payments, reverse transactions, or replace legal/compliance decisions.

Use at your own risk. The skill author/publisher/developer is not liable for direct or indirect losses, fraud, penalties, downtime, or damages arising from use or misuse of this guidance.

## Incident severity model

- `P0`: broad outage / incorrect success/failure state at scale
- `P1`: major degradation with partial workaround
- `P2`: limited impact to specific cohorts or features
- `P3`: minor issue, low customer impact

## Standard response workflow

1. **Acknowledge and assign roles**
   - incident commander
   - tech lead
   - comms owner
   - reconciliation owner

2. **Establish blast radius**
   - affected methods/regions/providers
   - impacted users/orders
   - error signatures and trend window

3. **Contain**
   - freeze risky deploys
   - enable degraded mode messaging
   - pause high-risk paths if needed

4. **Diagnose**
   - check webhook pipeline, API errors, queue lag, provider status
   - identify first failing component and triggering change

5. **Mitigate and recover**
   - apply safe rollback/fix
   - reconcile pending and mismatched states
   - verify customer-facing correctness

6. **Close and learn**
   - final incident summary
   - postmortem with owner/due-date action items

## Guardrails

- Never communicate "resolved" before metrics and correctness checks pass.
- Never run blind retries that can create duplicate charges.
- Always include transaction reference IDs in customer/support comms.
- Keep all decisions time-stamped in incident log.

## Output format

When invoked, return:

1. severity + current phase
2. top 3 immediate actions
3. customer impact summary
4. next update time and owner
5. reconciliation and correctness checklist

## Setup

Read [setup.md](setup.md) on first use.

## Validation

Run [validation-checklist.md](validation-checklist.md) for drills and live incidents.

## References

- Triage and mitigation templates: [incident-playbook.md](incident-playbook.md)
- Stakeholder/customer comms templates: [comms-templates.md](comms-templates.md)
- Post-incident tracking template: [postmortem-template.md](postmortem-template.md)
- Launch/readiness checks: [validation-checklist.md](validation-checklist.md)

