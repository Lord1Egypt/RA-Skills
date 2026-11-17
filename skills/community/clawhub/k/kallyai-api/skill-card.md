## Description:

KallyAI Executive Assistant handles outbound and inbound calls, email, bookings, research, errands, multi-channel messaging, phone number management, and related delegation tasks through a terminal CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sltelitsyn](https://clawhub.ai/user/sltelitsyn)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to delegate communications and operational tasks to KallyAI from Claude Code or a terminal, including calls, email, bookings, search, messaging, outreach, and account management.

### Deployment Geography for Use:

Global, subject to KallyAI country support restrictions.

## Known Risks and Mitigations:

Risk: The broad natural-language ask command can initiate real-world communications or account actions with unclear confirmation boundaries.

Mitigation: Confirm recipients, requested action, affected accounts, and expected outcome before running broad delegation commands.

Risk: The skill can access private communications and account-linked services through authenticated KallyAI sessions.

Mitigation: Install only when the user accepts that access, review connected accounts and scopes, and log out or disconnect services when no longer needed.

Risk: Some operations affect costs, subscriptions, phone numbers, channels, or other potentially irreversible account state.

Mitigation: Require explicit user approval for budgets, subscription changes, phone-number release, channel changes, and similarly consequential actions.

## Reference(s):

- [KallyAI API Reference](references/api-reference.md)
- [ClawHub release page](https://clawhub.ai/sltelitsyn/skills/kallyai-api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON CLI responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled CLI prints machine-readable JSON by default and supports human-readable tables with --human.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
