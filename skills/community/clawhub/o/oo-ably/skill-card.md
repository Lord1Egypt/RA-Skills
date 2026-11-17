## Description:

Use Ably through an OOMOL-connected account to read, publish, and manage channel data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to inspect Ably channel activity and statistics, publish messages, activate channels, and manage push subscriptions through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup can run downloaded software without prompting, and the remote installer behavior was not verified.

Mitigation: Review and approve CLI installation separately, preferably using a fixed release with verified integrity; check whether it installs or updates other agent skills.

Risk: The skill can publish messages and delete push notification subscriptions in the connected Ably account.

Mitigation: Limit the connected account's permissions and retain confirmation for write and destructive actions.

## Reference(s):

- [Ably](https://ably.com)
- [Ably REST API documentation](https://ably.com/docs/api/rest-api)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [JSON responses and shell commands with Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
