## Description:

Step-by-step onboarding guide for setting up a new AI Personal Assistant on OpenClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[netanel-abergel](https://clawhub.ai/user/netanel-abergel)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and PA owners use this skill to guide a new OpenClaw personal assistant through account creation, WhatsApp setup, integrations, configuration, and first-response verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The onboarding flow asks users to connect sensitive business accounts such as Google Calendar, Gmail, Drive, contacts, WhatsApp, and monday.com.

Mitigation: Grant the agent only the minimum permissions needed for each integration and require explicit owner approval before enabling optional briefing, directory, or public coordination steps.

Risk: The artifact shows a monday.com token being written to a plaintext credential file.

Mitigation: Use a secret manager or a hardened credential file with owner-only permissions, and avoid placing real tokens directly in shell commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/netanel-abergel/skills/pa-onboarding)
- [Publisher profile](https://clawhub.ai/user/netanel-abergel)
- [PA skills reference library](https://github.com/netanel-abergel/pa-skills)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with checklist items, tables, and inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One-step-at-a-time onboarding flow with confirmation before moving to later phases.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
