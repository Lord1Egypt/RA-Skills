---
name: meshmcp-remotescreen
description: Plan consent-based screen-support review steps for owned Android devices using only user-provided context, privacy boundaries, safe next steps, and stop conditions.
---

# Screen Support Review Planner

Use this skill to plan a consent-based screen-support session for an owned
Android device. Keep the work to a written support checklist based on
user-provided screenshots or descriptions.

## Inputs

Collect:

- device owner,
- support goal,
- consent statement,
- screenshot or description provided by the user,
- support boundaries,
- stop conditions.

Do not request credentials, device unlock codes, private notifications, payment
details, or private contact data.

## Workflow

1. Confirm the device owner and consent boundary.
2. Restate the support goal in plain language.
3. Identify what can be answered from the user-provided screenshot or text.
4. Produce a manual support checklist:
   - what the human should inspect,
   - what should be hidden before sharing,
   - what action should be skipped if consent is unclear,
   - when to stop and ask the owner.

## Output

Return:

- support summary,
- privacy checklist,
- safe next steps for the human,
- questions to resolve before continuing.

## Guardrails

- Keep device operation and observation outside this skill.
- Do not ask for unlock codes or private account data.
- Keep support supervised by the device owner.
- Keep user-facing instructions limited to the support steps the owner should see.
