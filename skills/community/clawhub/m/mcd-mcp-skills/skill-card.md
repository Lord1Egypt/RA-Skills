## Description:

Integrates with the McDonald's MCP platform so agents can query nutrition and menus, manage delivery addresses and coupons, calculate or create delivery orders, redeem points, and check campaign timing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moxin1044](https://clawhub.ai/user/moxin1044)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to operate McDonald's MCP account workflows, including food information lookup, delivery ordering, address and coupon management, loyalty point queries, and point redemptions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create real McDonald's account actions such as delivery orders, address creation, bulk coupon claims, and point redemptions.

Mitigation: Require explicit user confirmation immediately before any account-changing action.

Risk: The skill can handle delivery personal information, including addresses, phone numbers, contacts, and coordinates.

Mitigation: Avoid placing personal information in shell commands or persisted agent logs; collect and pass sensitive values through safer runtime channels when available.

Risk: The skill requires a McDonald's MCP token that authorizes actions on the connected account.

Mitigation: Install only when the operator accepts that account access, and rotate or revoke the token if it may have been exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/moxin1044/skills/mcd-mcp-skills)
- [McDonald's Open Platform](https://open.mcd.cn)
- [Tools parameter reference](references/tools_reference.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance]

**Output Format:** [Markdown with inline shell and Python command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MCD_MCP_TOKEN for live MCP calls.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
