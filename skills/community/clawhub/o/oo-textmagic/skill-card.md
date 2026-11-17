## Description:

Operate Textmagic contacts, lists, templates, and SMS messaging through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users can retrieve Textmagic account, contact, list, and template information, create contact lists, and send SMS messages through a connected Textmagic account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup fallback can execute a downloaded CLI installer without a separate approval step.

Mitigation: Review the installer and verify the CLI release; approve CLI installation separately before running it.

Risk: Sending SMS can reach up to 1,000 recipients and incur charges.

Mitigation: Confirm the exact recipients and message content, and review expected charges before sending.

## Reference(s):

- [Textmagic API documentation](https://docs.textmagic.com/)
- [Textmagic](https://www.textmagic.com/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Text, Guidance]

**Output Format:** [Structured connector results with concise text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creating contact lists and sending SMS messages are write actions that require user confirmation.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
