## Description:

Manage Make.com organizations, users, teams, scenarios, and billing. Configure organization settings, manage team members, retrieve usage analytics, and access pricing information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to administer Make.com organizations, users, teams, billing, usage analytics, and related platform settings through a connected Make account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill brokers access to a connected Make.com account through ClawLink, which can expose organization administration and account-level capabilities.

Mitigation: Install only if ClawLink is trusted, review Make OAuth permissions, use the least-privileged Make account practical, and revoke the connection when it is no longer needed.

Risk: Write operations can change organizations, users, or account-related settings.

Mitigation: Require explicit user confirmation, review previews carefully before execution, and confirm destructive or password-reset actions before running them.

## Reference(s):

- [Make API Documentation](https://www.make.com/en/api-docs)
- [Make Help Center](https://www.make.com/en/help)
- [ClawLink OpenClaw Docs](https://docs.claw-link.dev/openclaw)
- [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=make-automation)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline shell commands and tool-call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses live ClawLink tool discovery and previews before write actions.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
