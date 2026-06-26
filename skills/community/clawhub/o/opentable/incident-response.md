# Incident Response - OpenTable

## Incident Classes

| Class | Typical Symptom | Immediate Priority |
|------|------------------|--------------------|
| Overbooking | More covers than seatable capacity | Protect in-house service and communicate options |
| Confirmation failure | Guests claim no confirmation or wrong time | Reconcile reservation state and reduce arrival friction |
| Availability mismatch | Slots shown despite operational block | Stop new exposure and correct inventory quickly |
| Outage or degraded platform | Booking flow unavailable or unstable | Activate fallback intake and preserve guest trust |

## First 30 Minutes

1. Define scope: which dates, times, and parties are affected.
2. Freeze risky inventory changes until facts are clear.
3. Trigger guest communication template with plain-language options.
4. Establish fallback path (phone, waitlist, alternate slot offer).
5. Assign one owner for timeline updates and internal coordination.

## Guest Communication Rules

- State what happened and what is being done now.
- Offer concrete alternatives, not generic apologies.
- Confirm next touchpoint time when resolution is not immediate.
- Keep high-friction guests in priority queue until resolved.

## Recovery and Prevention

- Log root cause with evidence.
- Record mitigation steps and whether they worked.
- Add one preventive control tied to that root cause.
- Review if policy or pacing design increased blast radius.

## Post-Incident Questions

- What early signal was missed?
- Which decision increased guest impact?
- Which fallback worked fastest with least confusion?
- What should become a default playbook step?
