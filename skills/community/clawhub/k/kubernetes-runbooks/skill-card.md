## Description:

一个基于模型上下文协议(MCP)的服务器，提供对Kubernetes故障排除手册的访问，支持搜索、内容获取和AI集成。

This skill is ready for commercial/non-commercial use.

## Publisher:

[cainingnk](https://clawhub.ai/user/cainingnk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and platform engineers use this skill to search Kubernetes troubleshooting runbooks, list available topics, and fetch a specific runbook through an external MCP API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary reports mismatched Gaokao/XBY code in a skill described as Kubernetes runbook tooling.

Mitigation: Review the source before installation and prefer a version that removes the mismatch.

Risk: The skill persists the Xiaobenyang API key in a plaintext .env file.

Mitigation: Use a low-scope API key and avoid running the skill in repositories where .env files may be committed or shared.

Risk: The skill depends on an external HTTPS API endpoint for runbook content.

Mitigation: Verify the endpoint is the intended host, validate outbound destinations, and pin dependencies before deployment.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/cainingnk/skills/kubernetes-runbooks)
- [Xiaobenyang API key portal](https://xiaobenyang.com)
- [Xiaobenyang MCP API endpoint](https://mcp.xiaobenyang.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, API Calls]

**Output Format:** [Markdown or structured text summarizing JSON responses from the upstream runbook API]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an XBY API key and network access to the Xiaobenyang MCP API.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
