## Description: <br>
GitHub MCP Server enables AI agents to manage repositories, read and update files, handle issues and pull requests, manage branches, and automate GitHub workflows through the GitHub API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BuddhaSource](https://clawhub.ai/user/BuddhaSource) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering teams use this skill to connect agents to GitHub for repository operations, file changes, issue and pull request management, branch work, code search, and release automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables powerful repository-write operations with too few built-in guardrails. <br>
Mitigation: Require explicit human approval before file writes, branch merges, releases, repository creation, or bulk issue and pull request changes. <br>
Risk: Over-broad GitHub credentials could expose repositories or allow unintended changes. <br>
Mitigation: Use fine-grained tokens limited to specific repositories and permissions, and prefer read-only access for browsing tasks. <br>
Risk: The referenced MCP server package or implementation could change independently of this skill. <br>
Mitigation: Install only trusted implementations and pin and verify the MCP package where possible. <br>


## Reference(s): <br>
- [MCP Registry](https://registry.modelcontextprotocol.io/) <br>
- [Archived Model Context Protocol GitHub Server](https://github.com/modelcontextprotocol/servers-archived) <br>
- [GitHub REST API Documentation](https://docs.github.com/en/rest) <br>
- [GitHub REST API Rate Limits](https://docs.github.com/en/rest/overview/rate-limits-for-the-rest-api) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides MCP client setup and agent GitHub automation workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
