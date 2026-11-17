## Description:

Use Raisely to read campaign and fundraising profile data and manage webhooks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Raisely account users and fundraising teams can retrieve campaign, profile, and webhook information and manage webhooks through a connected Raisely account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup directs the agent to run a remote installer that has not been verified.

Mitigation: Review and approve the installer before use, including any automatic changes it may make to other agent skills.

Risk: Webhook actions can change or delete account configuration.

Mitigation: Review the action schema and confirm the exact target and effect before running a webhook change.

## Reference(s):

- [Raisely](https://raisely.com/)
- [Raisely API documentation](https://raisely.com/developers)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [Raisely on ClawHub](https://clawhub.ai/oomol/skills/oo-raisely)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Text and JSON responses with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
