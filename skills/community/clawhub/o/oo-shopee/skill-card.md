## Description:

Use this skill to read, create, update, and delete Shopee data through the oo CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users can inspect Shopee shops, products, orders, returns, and shipping, and create products, ship orders, upload images, or update prices and stock through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can run installer code fetched remotely, whose contents were unavailable for review.

Mitigation: Review setup first, use a verified CLI release, and decide whether it may install or synchronize additional agent skills.

Risk: Writes can ship orders or change product prices and stock in a live Shopee account.

Mitigation: Confirm the exact target and payload before each write, and get explicit approval before changes or overwrites.

## Reference(s):

- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [Shopee API documentation](https://open.shopee.cn/developer-guide/14)
- [Shopee](https://www.shopee.com/)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Shell commands with JSON payloads and JSON responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action inputs depend on the live connector schema.]

## Skill Version(s):

1.0.2 (source: frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
