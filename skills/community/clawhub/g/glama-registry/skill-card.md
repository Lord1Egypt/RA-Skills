## Description:

提供MCP注册服务器的搜索功能，用于查询匹配特定字符串的MCP服务器。

This skill is ready for commercial/non-commercial use.

## Publisher:

[alinklab](https://clawhub.ai/user/alinklab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to search the Glama MCP registry for MCP servers that match a query string through the XiaoBenYang API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores the XiaoBenYang API key in plaintext in a .env file.

Mitigation: Use a temporary or low-privilege key and confirm that .env is not committed, shared, or included in generated artifacts.

Risk: The API key can be sent to a configurable upstream API endpoint.

Mitigation: Verify the configured XBY_GAOKAO_BASE_URL before use and avoid running the skill if the endpoint is untrusted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alinklab/skills/glama-registry)
- [XiaoBenYang API key site](https://xiaobenyang.com)
- [XiaoBenYang MCP API endpoint](https://mcp.xiaobenyang.com)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON results summarized in Markdown or plain text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an XBY_APIKEY value and sends search requests to a configurable upstream API endpoint.]

## Skill Version(s):

1.0.1 (source: server release metadata; SKILL.md frontmatter remains 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
