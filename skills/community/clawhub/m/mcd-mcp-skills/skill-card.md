## Description: <br>
Integrates with the McDonald's China MCP service so an agent can look up nutrition and menus, manage delivery addresses and coupons, calculate prices, create delivery orders, query orders, and redeem loyalty points. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[moxin1044](https://clawhub.ai/user/moxin1044) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to interact with McDonald's China services for nutrition lookup, delivery ordering, address management, coupon handling, loyalty point balance checks, and point redemption. It is appropriate when the user has configured an MCD_MCP_TOKEN and explicitly wants the agent to perform McDonald's account or ordering tasks. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses MCD_MCP_TOKEN to access the user's McDonald's MCP account. <br>
Mitigation: Install only when the publisher and the McDonald's MCP service are trusted with that account token. <br>
Risk: Mutating actions can create delivery orders, add addresses, claim coupons, or redeem loyalty points. <br>
Mitigation: Require explicit user confirmation before any mutating action, especially from ambiguous prompts. <br>
Risk: Ordering and address workflows may expose or change personal delivery details such as address, contact name, phone number, selected items, coupons, total price, and loyalty point deductions. <br>
Mitigation: Confirm these details with the user before submitting requests and avoid sharing generated order or account output beyond the intended conversation. <br>


## Reference(s): <br>
- [mcd-mcp-skills ClawHub page](https://clawhub.ai/moxin1044/mcd-mcp-skills) <br>
- [Publisher profile](https://clawhub.ai/user/moxin1044) <br>
- [McDonald's China Open Platform](https://open.mcd.cn) <br>
- [McDonald's MCP service](https://mcp.mcd.cn) <br>
- [Tool parameter reference](artifact/references/tools_reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or text guidance with shell command examples and JSON-style service responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MCD_MCP_TOKEN and sends authorized requests to the McDonald's MCP service; some commands can create orders, add addresses, claim coupons, or redeem loyalty points.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
