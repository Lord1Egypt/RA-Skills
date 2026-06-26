## Description: <br>
Gurkerl.at grocery shopping via MCP - search products, manage cart, orders, recipes, favorites. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[florianbeer](https://clawhub.ai/user/florianbeer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to search Gurkerl.at products, manage carts, review orders, browse recipes, and interact with grocery-shopping account workflows through the official MCP server. <br>

### Deployment Geography for Use: <br>
Austria <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses account password environment variables and shows a persistent systemd configuration path that can store credentials. <br>
Mitigation: Protect any service configuration containing credentials, avoid persistent password storage unless necessary, and install only after verifying the Gurkerl CLI and MCP endpoint. <br>
Risk: The available tools can place orders, change checkout payment or delivery details, cancel orders, file claims, request credits, adjust deposits, and send support email. <br>
Mitigation: Require explicit user confirmation before order, payment, delivery, cancellation, claim, credit, deposit, or support-email actions. <br>


## Reference(s): <br>
- [Gurkerl MCP server page](https://www.gurkerl.at/seite/mcp-server) <br>
- [ClawHub Gurkerl skill page](https://clawhub.ai/florianbeer/gurkerl) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/florianbeer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON tool examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and jq, plus GURKERL_EMAIL and GURKERL_PASS environment variables.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
