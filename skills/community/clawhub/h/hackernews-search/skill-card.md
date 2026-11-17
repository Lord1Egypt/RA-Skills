## Description:

一个通过Model Context Protocol提供HackerNews内容搜索、检索和分析的服务，适用于AI代理和开发者。

This skill is ready for commercial/non-commercial use.

## Publisher:

[cainingnk](https://clawhub.ai/user/cainingnk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agents use this skill to search Hacker News content, inspect front-page and recent posts, retrieve item discussion trees, and look up public user profiles through the configured API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires an XBY_APIKEY for a third-party backend that is under-explained in the release evidence.

Mitigation: Only provide the API key after trusting xiaobenyang.com with the key and query parameters.

Risk: The skill stores XBY_APIKEY in a local .env file in plaintext.

Mitigation: Prefer an updated release that avoids persistent plaintext secrets, or remove the .env value when the skill is no longer needed.

Risk: The release evidence recommends clearer backend documentation and pinned dependencies.

Mitigation: Review the backend behavior and dependency set before installing or deploying the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cainingnk/skills/hackernews-search)
- [XiaoBenYang API key portal](https://xiaobenyang.com)
- [XiaoBenYang MCP API endpoint](https://mcp.xiaobenyang.com)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, configuration guidance]

**Output Format:** [Markdown summaries of JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an XBY_APIKEY before making upstream requests.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
