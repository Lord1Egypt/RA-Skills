## Description:

Use Landbot to read customer and channel data, send customer messages, and update customer fields through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use the skill to inspect Landbot customers, channels, and message history, and to send messages or update customer fields through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The required CLI can make broader agent changes than the skill explains, and its installer and deployed connector were not verified.

Mitigation: Review and verify a specific CLI release before setup; consider disabling startup skill synchronization with OO_SKILLS_SYNC_DISABLED=1.

Risk: Customer data passes through OOMOL, and actions can send messages or change customer fields.

Mitigation: Connect only the necessary Landbot permissions and keep user confirmation for message sends and field changes.

## Reference(s):

- [Landbot API documentation](https://dev.landbot.io/api-reference/introduction)
- [Landbot](https://landbot.io)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API calls, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON action payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Write actions require confirmation; fetch each action schema before constructing its payload.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
