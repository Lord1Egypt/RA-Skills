## Description:

Creates Guoguo shipping pickup orders through an MCP-connected Guoguo send service after collecting sender, receiver, account, address, and pickup-time details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dazhanggui](https://clawhub.ai/user/dazhanggui)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to gather required shipping details and create a Guoguo pickup order for a two-hour service window. The skill also guides MCP connection setup or checks before order creation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup step may persistently modify MCP configuration through a setup script that is not included in the artifact.

Mitigation: Require explicit user approval before setup, show the exact MCP configuration change, and include the setup script for review before use.

Risk: The order workflow handles personal shipping details such as names, phone numbers, and full addresses.

Mitigation: Use the skill only with a trusted MCP server and collect or transmit only the information needed to create the shipment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dazhanggui/skills/guoguo)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON request examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include MCP tool arguments containing names, phone numbers, full addresses, pickup timestamps, and order response fields.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
