## Description:

Outclaw Setup helps an agent inventory outreach plugins, connect outreach channels, capture user and organization profile knowledge, and prepare per-channel writing style setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[milstan](https://clawhub.ai/user/milstan)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to prepare an OutClaw outreach workspace by checking available tools, connecting communication channels, capturing user and company context, and handing off style learning before outreach planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can connect business communication accounts and install third-party outreach plugins with broad authority.

Mitigation: Approve each integration separately, verify plugin source and requested permissions before authentication, and keep skipped channels disabled.

Risk: The skill stores user profile, organization context, setup state, plugin status, and fetched website content locally.

Mitigation: Review retained files for sensitive content, restrict workspace access, and remove local profile or raw website captures that should not persist.

Risk: OAuth callback URLs or credentials shared through chat can expose authentication material.

Mitigation: Use transport-aware OAuth links, avoid pasting full callback URLs when possible, and verify connection status after authentication instead.

Risk: Optional recurring prospecting jobs can repeatedly access lead and outreach tooling after setup.

Mitigation: Enable schedules only with explicit user approval, document the cadence, and keep generated outreach queued for review rather than automatic sending.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/milstan/skills/outclaw-setup)
- [OutClaw homepage](https://github.com/leadbay/outclaw)
- [Inventory check](references/inventory-check.md)
- [Plugin connection flows](references/plugin-connect.md)
- [Capturing the user's profile into kb/me/](references/user-profile.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, status summaries, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setup state, local knowledge-base entries, plugin setup logs, and channel style-learning handoff guidance when used by an agent.]

## Skill Version(s):

1.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
