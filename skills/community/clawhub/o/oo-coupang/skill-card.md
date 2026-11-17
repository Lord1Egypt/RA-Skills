## Description:

Coupang (coupang.com). Use this skill for ANY Coupang request — reading, creating, updating, and deleting data. Whenever a task involves Coupang, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Coupang sellers and their agents can retrieve order, product, inventory, price, and return information through an OOMOL-connected Coupang account. They can also update item prices and inventory quantities, with confirmation required before changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic CLI setup may install or update software, including skills used by other agents; external installers and the hosted connector implementation have not been verified.

Mitigation: Review and approve CLI installation separately, check what it will install or update, and use the publisher's synchronization controls if unwanted.

Risk: Price and inventory updates can overwrite Coupang seller data.

Mitigation: Use an appropriately restricted Coupang account and confirm the exact target and values before running an update.

## Reference(s):

- [Coupang API documentation](https://developers.coupang.com/en/api)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [Coupang skill release on ClawHub](https://clawhub.ai/oomol/skills/oo-coupang)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [JSON results and concise text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can read seller data and propose price or inventory updates; state changes require explicit user confirmation.]

## Skill Version(s):

1.0.5 (source: frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
