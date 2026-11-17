## Description:

Automate order routing, fulfillment, and inventory management across channels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ncreighton](https://clawhub.ai/user/ncreighton)

### License/Terms of Use:

MIT-0

## Use Case:

E-commerce operators, fulfillment teams, and developers use this skill to design order-routing, inventory-sync, notification, and exception-handling workflows across stores, warehouses, carriers, Slack, and Google Sheets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install an unpinned global orderflow-cli package.

Mitigation: Verify the package source and version before installation, and install or test it in a sandboxed environment first.

Risk: The skill connects commerce, warehouse, carrier, sheet, and notification credentials to automations that can trigger live fulfillment actions.

Mitigation: Use least-privilege service accounts, test with non-production integrations, and require human review before activating live workflows.

Risk: Setup examples include secrets passed through command-line authentication flows.

Mitigation: Rotate any secrets entered during setup and prefer secure environment or secret-management workflows for production use.

## Reference(s):

- [Orderflow ClawHub skill page](https://clawhub.ai/ncreighton/skills/orderflow)
- [ncreighton publisher profile](https://clawhub.ai/user/ncreighton)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces workflow designs, configuration examples, setup commands, routing decisions, inventory reports, and alert content for review before execution.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
