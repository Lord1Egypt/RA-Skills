## Description:

Use Picky Assist to check account balances and send messages through a connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Users and developers use this skill to read a connected Picky Assist account balance or submit text and public URL media messages. Review the recipients and message content before submitting a message.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup directs the agent to execute downloaded software that was not verified for this release.

Mitigation: Review and separately approve the CLI installation; prefer a pinned, verified release and check whether it installs other agent skills.

Risk: Sending a message can disclose content to unintended recipients.

Mitigation: Confirm recipients and message content before sending.

## Reference(s):

- [Picky Assist](https://pickyassist.com/)
- [Picky Assist API documentation](https://help.pickyassist.com/api-documentation-v2/introduction)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [JSON connector responses and concise action results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Message submissions are accepted for processing; delivery is not guaranteed.]

## Skill Version(s):

1.0.2 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
