## Description: <br>
Places McDonald's China delivery orders through the official MCP server using a Bearer MCP token, including address lookup, menu browsing, price calculation, order creation, status checks, and coupon or points queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[danielliao](https://clawhub.ai/user/danielliao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to connect an agent or MCP client to McDonald's China ordering workflows for menu lookup, delivery address selection, price checks, order creation, and order status follow-up. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create or cancel real McDonald's China orders when supplied with a valid MCP bearer token. <br>
Mitigation: Require explicit final user confirmation before create-order or cancellation actions, and show the calculated payable amount before order creation. <br>
Risk: The skill sends delivery details, contact information, addresses, coordinates, and account/order data to the remote service during supported workflows. <br>
Mitigation: Use the skill only with users who understand the data flow, avoid unnecessary address or location lookups, and keep sensitive results out of logs and shared transcripts. <br>
Risk: The bearer token grants account and order authority, and the client allows the MCP endpoint to be overridden through MCD_MCP_URL. <br>
Mitigation: Store MCD_MCP_TOKEN securely, do not expose it in prompts or logs, and keep MCD_MCP_URL fixed to https://mcp.mcd.cn unless the endpoint has been independently trusted. <br>


## Reference(s): <br>
- [McDonald's MCP quick reference](artifact/references/api.md) <br>
- [McDonald's China MCP endpoint](https://mcp.mcd.cn) <br>
- [ClawHub skill page](https://clawhub.ai/danielliao/mcdonalds-mcp-order-lite) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with JSON tool results and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return order IDs, payment URLs, store/menu data, address-related fields, coupon data, and status summaries from the remote MCP service.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
