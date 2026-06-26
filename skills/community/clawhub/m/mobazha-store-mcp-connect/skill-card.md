## Description: <br>
Connect an AI agent to a Mobazha store via MCP (Model Context Protocol). Use when the user wants their agent to directly manage store products, orders, and settings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fengzie](https://clawhub.ai/user/fengzie) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Store owners, operators, and developers use this skill to connect an AI agent to a Mobazha store so it can help manage products, orders, messages, discounts, collections, profiles, notifications, search, and finance-related store workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The connected agent can have persistent control over products, orders, refunds, customer messages, and store settings. <br>
Mitigation: Install only when agent administration is intended, use scoped or temporary tokens where possible, and require manual confirmation for refunds, deletions, buyer messages, profile changes, and other business-impacting actions. <br>
Risk: API tokens or token-bearing MCP configuration can expose store access if committed, logged, or shared. <br>
Mitigation: Store tokens in environment variables or a secrets manager, keep token-bearing config files out of git, avoid displaying tokens, and revoke tokens when access is no longer needed. <br>
Risk: Remote or non-HTTPS store connections can expose credentials or administrative traffic. <br>
Mitigation: Prefer HTTPS for store endpoints and use an SSH or VPN tunnel for remote VPS access when appropriate. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fengzie/mobazha-store-mcp-connect) <br>
- [Publisher profile](https://clawhub.ai/user/fengzie) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with MCP configuration examples, JSON snippets, shell commands, and troubleshooting guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Mobazha API token and may optionally use SSH credentials for tunneled remote store connections.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
