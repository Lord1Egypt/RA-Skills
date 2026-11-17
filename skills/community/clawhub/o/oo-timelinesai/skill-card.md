## Description:

Use an OOMOL-connected TimelinesAI workspace to inspect chats, messages, workspace details, and delivery status, and to send WhatsApp messages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and customer support teams can review TimelinesAI conversations, check workspace and message status, and send WhatsApp messages through an already connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The remote CLI installer was unavailable for inspection, so its behavior has not been established.

Mitigation: Review and approve a specific CLI release before automatic setup, including any additional agent skills it installs.

Risk: Sending a WhatsApp message changes external state.

Mitigation: Confirm the exact message payload and effect with the user before sending.

## Reference(s):

- [TimelinesAI](https://timelines.ai/)
- [TimelinesAI API documentation](https://timelinesai.mintlify.app/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [JSON connector results and plain-text WhatsApp message content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
