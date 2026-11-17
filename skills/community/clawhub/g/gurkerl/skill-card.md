## Description:

Gurkerl.at grocery shopping via MCP - search products, manage cart, orders, recipes, favorites.

This skill is ready for commercial/non-commercial use.

## Publisher:

[florianbeer](https://clawhub.ai/user/florianbeer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to interact with Gurkerl.at grocery delivery through MCP, including product search, cart management, checkout, order management, recipes, favorites, and customer-care workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a reusable Gurkerl account password through GURKERL_PASS and documents persistent storage in a user service override.

Mitigation: Use a dedicated account where possible, protect local credential files with strict permissions, and do not commit, paste, or share the service override.

Risk: The available tools can submit checkout, update payment method, repeat or cancel orders, change delivery timeslots, and modify cart or order contents.

Mitigation: Require explicit user review and confirmation before any checkout, payment, order cancellation, reorder, delivery-slot change, or cart-clearing action.

Risk: The skill can delete shopping lists and send support email or customer-care requests on the user's behalf.

Mitigation: Treat list deletion and customer-care messaging as irreversible or externally visible actions and confirm the exact content and target before execution.

## Reference(s):

- [Gurkerl MCP server](https://www.gurkerl.at/seite/mcp-server)
- [ClawHub skill page](https://clawhub.ai/florianbeer/skills/gurkerl)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash, INI, and JSON command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and jq plus GURKERL_EMAIL and GURKERL_PASS for authenticated account access.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
