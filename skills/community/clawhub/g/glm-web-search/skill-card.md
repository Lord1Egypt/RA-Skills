## Description:

GLM Web Search helps agents configure and call BigModel's GLM web search MCP server for current web search results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thincher](https://clawhub.ai/user/thincher)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to connect OpenClaw or a compatible agent environment to BigModel's GLM web search MCP server, then issue search queries for current web information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API key exposure or leakage during configuration.

Mitigation: Store the key in a protected secret store or owner-only configuration file, avoid putting the key in a URL, and rotate any key previously configured that way.

Risk: Runtime dependency risk from installing or invoking mcporter through npx.

Mitigation: Use a version-pinned, reviewed mcporter install before adding or calling the MCP server.

Risk: The skill sends search queries to GLM/BigModel's hosted web search service.

Mitigation: Use it only when GLM/BigModel is an acceptable search provider for the query content and environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thincher/skills/glm-web-search)
- [Official GLM Search MCP Server documentation](https://docs.bigmodel.cn/cn/coding-plan/mcp/search-mcp-server)
- [BigModel GLM Coding API key page](https://www.bigmodel.cn/glm-coding?ic=OOKF4KGGTW)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes MCP setup steps, API key configuration guidance, and example web search calls.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
