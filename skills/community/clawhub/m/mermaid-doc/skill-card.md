## Description:

Mermaid Doc MCP Server是一个用于生成Mermaid文档的服务器，提供列出可用图表和检索特定图表文档的功能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[alinklab](https://clawhub.ai/user/alinklab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and documentation authors use this skill to retrieve Mermaid diagram documentation for supported diagram types and present the returned content to users.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan says the skill requires a XiaoBenYang API key, stores it in plaintext in a local .env file, and sends requests through a XiaoBenYang MCP endpoint.

Mitigation: Install only after accepting that secret-handling model; prefer a secure secret store, restrict access to the .env file, and review endpoint use before deployment.

Risk: The security scan reports leftover Gaokao/XiaoBenYang configuration in a skill presented as a Mermaid documentation helper.

Mitigation: Review the unrelated configuration and documentation before use, and require cleanup or publisher clarification for production environments.

## Reference(s):

- [Mermaid Doc skill page](https://clawhub.ai/alinklab/skills/mermaid-doc)
- [ALinkLab publisher profile](https://clawhub.ai/user/alinklab)
- [XiaoBenYang API key site](https://xiaobenyang.com)
- [XiaoBenYang MCP endpoint](https://mcp.xiaobenyang.com)

## Skill Output:

**Output Type(s):** [API Calls, Markdown, Guidance]

**Output Format:** [Markdown or text summary derived from upstream JSON responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a XiaoBenYang API key before calling the Mermaid documentation tool.]

## Skill Version(s):

1.0.1 (source: server release metadata; SKILL.md frontmatter remains 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
