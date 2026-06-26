## Description: <br>
Verifies and configures required MCP servers for the Product Guide Writer workflow, especially Atlassian and GitHub integrations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tsvetelin-kulinski](https://clawhub.ai/user/tsvetelin-kulinski) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and documentation authors use this skill to verify Atlassian and GitHub MCP setup for the Product Guide Writer workflow and receive configuration guidance when servers, credentials, or Confluence access are missing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow involves sensitive GitHub, Atlassian, Figma, or Elasticsearch credentials. <br>
Mitigation: Use least-privilege access, avoid pasting tokens into chat or logs, and configure optional integrations only when needed. <br>
Risk: Incorrect MCP package names, endpoints, or workspace permissions can cause failed setup or unintended access. <br>
Mitigation: Verify MCP package names and endpoints before use, then run the documented connection and permission checks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tsvetelin-kulinski/github-mpc) <br>
- [Publisher profile](https://clawhub.ai/user/tsvetelin-kulinski) <br>
- [Atlassian remote MCP endpoint](https://mcp.atlassian.com/v1/mcp) <br>
- [GitHub personal access tokens](https://github.com/settings/tokens) <br>
- [Trading212 GT Confluence space](https://trading212.atlassian.net/wiki/spaces/gt) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with checklists, JSON snippets, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes validation steps for required and optional MCP servers.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
