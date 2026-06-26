## Description: <br>
Search, read, and work with Shopify products, orders, customers, and shop data through a local MCP wrapper. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maverick](https://clawhub.ai/user/maverick) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Shopify operators and developers use this skill to inspect and manage products, orders, customers, and store data from an agent through a local MCP wrapper. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad Shopify admin access, including access to sensitive commerce data and live store changes. <br>
Mitigation: Use a narrowly scoped Shopify token, avoid production write permissions unless needed, and require explicit human approval before product mutations or raw admin_graphql calls. <br>
Risk: Write operations can create, publish, update, or expose products, variants, orders, customers, or externally visible product links. <br>
Mitigation: Confirm clear user intent before write tools, search before assuming product or variant IDs, and read product or variant details before recommending or linking items. <br>
Risk: The install metadata uses an unpinned mcporter package, which may not meet strict supply-chain controls. <br>
Mitigation: Pin or override the mcporter install version in controlled deployments. <br>
Risk: Shopify access token and shop environment variables are sensitive credentials. <br>
Mitigation: Provide credentials through secret management and avoid passing unrelated sensitive content through the Shopify tools. <br>


## Reference(s): <br>
- [Maverick Shopify MCP on ClawHub](https://clawhub.ai/maverick/maverick-shopify-mcp) <br>
- [mcporter MCP CLI](https://github.com/steipete/mcporter) <br>
- [uv Documentation](https://docs.astral.sh/uv/) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [JSON responses from MCP tool calls, with Markdown or shell commands when the agent explains setup or invocation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Shopify shop and access token environment variables; tool result size depends on Shopify query limits and requested records.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
