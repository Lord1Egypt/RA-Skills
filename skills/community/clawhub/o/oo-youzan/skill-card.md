## Description:

Search and read Youzan shop data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Store operators and assistants use this skill to retrieve shop, product, order, delivery, inventory, and refund information from a connected Youzan account. It is intended for read actions using the oo CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can execute downloaded software without first requesting approval; the external installer and live connector have not been verified.

Mitigation: Review and approve CLI installation separately, including any bundled agent-skill changes.

Risk: The connected Youzan shop may expose sensitive business data.

Mitigation: Connect only the intended Youzan shop and consider the sensitivity of the accessible data.

## Reference(s):

- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)
- [Youzan](https://www.youzan.com/)
- [Youzan API documentation](https://doc.youzanyun.com/v2/doc/kdt_id)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [Youzan action data in JSON, with concise text summaries as needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returned fields vary by selected read action.]

## Skill Version(s):

1.0.5 (source: SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
