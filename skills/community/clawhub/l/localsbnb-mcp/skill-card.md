## Description: <br>
Guides agents and users in configuring the localsbnb-mcp-server npm package to query LocalsBnb/Lukeyun room status, room rates, orders, and operational data through the official API using user-provided APP_ID and APP_SECRET. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[localsbnb](https://clawhub.ai/user/localsbnb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Hotel and homestay operators, support teams, and developers use this skill to configure MCP access to LocalsBnb/Lukeyun business data and route room status, pricing, order, and operational questions to the correct tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The MCP server requires APP_ID and APP_SECRET credentials that could expose LocalsBnb account data if shared or committed. <br>
Mitigation: Provide credentials only through the MCP client's environment configuration, avoid public chats and repositories, prefer least-privilege read-only tokens where possible, and rotate exposed credentials. <br>
Risk: The skill runs an external npm package through npx, so package trust and version drift affect runtime behavior. <br>
Mitigation: Install only when the publisher and npm package are trusted, consider pinning the npm package version, and review updates before deployment. <br>
Risk: Order and business-data queries can include sensitive operational details and guest names, including masked names. <br>
Mitigation: Use accounts with appropriate permissions, keep outputs in controlled environments, and preserve order identifiers with guest-name fields without unnecessary redistribution. <br>


## Reference(s): <br>
- [localsbnb-mcp-server npm package](https://www.npmjs.com/package/localsbnb-mcp-server) <br>
- [LocalsBnb MCP on ClawHub](https://clawhub.ai/localsbnb/localsbnb-mcp) <br>
- [localsbnb publisher profile](https://clawhub.ai/user/localsbnb) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, Shell commands] <br>
**Output Format:** [Markdown with JSON configuration snippets and inline command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires APP_ID and APP_SECRET environment variables and uses npx to run the published localsbnb-mcp-server package.] <br>

## Skill Version(s): <br>
1.0.1 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
