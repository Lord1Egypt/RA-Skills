# Kimi Safety Workflows

## Safe-Send Checklist

Before sending anything non-trivial to Kimi, verify:

1. Does the prompt contain secrets, access tokens, or internal hostnames?
2. Does it include customer identifiers or contract-sensitive text?
3. Can the task succeed with a redacted or metadata-only version?
4. Does the user want this exact content to leave the machine?
5. Is there a cost cap or retry limit for batch work?

If any answer is unclear, stop and ask before sending.

## Recommended Trust Pattern

For recurring operational use:
- keep raw source material local
- send sanitized excerpts or summaries first
- store only the rule about what may leave the machine
- require explicit approval before first sensitive send

## Safer Workflow Patterns

| Situation | Safer move |
|-----------|------------|
| Incident notes with secrets | redact locally, then send the smallest useful excerpt |
| Ticket triage at scale | send metadata first, full body only on escalation |
| Public-facing draft generation | create an internal summary locally, then send a sanitized brief |
| New batch workflow | cap requests, retries, and total spend before first run |
| Debug logging | save only sanitized payloads and exact error class |

## Approval Language

When risk exists, make the boundary explicit:
- what will be sent
- why it needs to be sent
- what was removed locally
- whether the pattern should be remembered for next time
