## Description:

Use this skill to read Walmart Marketplace data and manage inventory through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Walmart Marketplace sellers use the skill to inspect inventory, catalog items, and purchase orders, and to replace inventory quantities for a seller SKU through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup executes unverified remote code and may install other agent skills; installation effects are unclear.

Mitigation: Verify and install a specific oo CLI release, and review its automatic skill installation behavior before enabling this skill.

Risk: An inventory update replaces the quantity for the selected seller SKU.

Mitigation: Review and approve the exact SKU and replacement quantity before running update_inventory.

## Reference(s):

- [Walmart Marketplace](https://marketplace.walmart.com)
- [Walmart Developer Documentation](https://developer.walmart.com/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Structured JSON data with concise text summaries and shell commands for actions]

**Output Parameters:** [Varies by requested Walmart Marketplace action and data]

**Other Properties Related to Output:** [Inventory updates replace the quantity for a seller SKU.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
