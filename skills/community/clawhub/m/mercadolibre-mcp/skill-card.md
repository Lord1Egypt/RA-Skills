## Description: <br>
Complete MCP server for Mercado Libre seller operations: products, orders, pricing, stock, questions, ads, reputation, and competitor analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[marcosnahuel](https://clawhub.ai/user/marcosnahuel) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Mercado Libre sellers and developers use this MCP server to let an agent inspect seller account data and perform operational tasks such as listing products, reviewing orders, updating price or stock, answering buyer questions, managing ads, and checking reputation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The server can change live listings, stock, buyer-question responses, and Product Ads for a Mercado Libre seller account. <br>
Mitigation: Use an MCP client or workflow that requires explicit approval before every write action, and scope credentials to the intended seller account. <br>
Risk: The security summary reports that part of a refreshed credential can be logged to stderr. <br>
Mitigation: Keep credentials in secret storage, avoid shared or retained stderr logs, and rotate tokens if token prefixes may already have been logged. <br>
Risk: The skill requires Mercado Libre OAuth credentials or an access token to operate on seller data. <br>
Mitigation: Provide credentials only in trusted runtime environments and avoid committing or sharing MCP configuration files that contain secrets. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/marcosnahuel/mercadolibre-mcp) <br>
- [Publisher profile](https://clawhub.ai/user/marcosnahuel) <br>
- [Project homepage](https://github.com/MarcosNahuel/mercadolibre-mcp) <br>
- [Mercado Libre developer portal](https://developers.mercadolibre.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration, guidance] <br>
**Output Format:** [MCP tool responses as text, with setup examples in JSON or shell-oriented configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Tools may read seller data or perform write actions against a configured Mercado Libre seller account.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
