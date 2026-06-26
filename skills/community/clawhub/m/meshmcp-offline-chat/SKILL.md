---
name: meshmcp-offline-chat
description: Plan a public-safe offline message test checklist for owned Android devices, including consent boundaries, non-sensitive sample text, success criteria, and human verification steps.
---

# Offline Message Test Planner

Use this skill to plan a small offline messaging test on owned devices. Keep the
work to written preparation, sample text, and human verification.

## Inputs

Collect:

- number of owned test devices,
- expected offline setting,
- message examples,
- consent and privacy boundaries,
- success criteria for the test.

Do not collect private message logs, device identifiers, contact lists, or
credential material.

## Workflow

1. Confirm all devices are owned or explicitly authorized for testing.
2. Define the offline test scenario and expected result.
3. Prepare short, non-sensitive sample messages.
4. Create a manual verification checklist:
   - devices ready,
   - privacy boundary confirmed,
   - sample message prepared,
   - result recorded by the human tester.

## Output

Return:

- test plan,
- sample non-sensitive messages,
- manual verification checklist,
- privacy notes,
- stop conditions.

## Guardrails

- Keep device and network operation outside this skill.
- Do not ask for private message content.
- Do not recommend using this with unknown or non-consenting devices.
