## Description:

通过百度 AI 搜索 API 进行网页搜索，获取实时信息和搜索结果。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yky3489](https://clawhub.ai/user/yky3489)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to query Baidu AI Search for current Chinese web results, with optional recency and site filters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A startup path can expose an unauthenticated API-key-backed search service to the network.

Mitigation: Keep the service bound to 127.0.0.1 and avoid the direct module __main__ path unless its bind address is fixed.

Risk: The application logs user queries.

Mitigation: Avoid searching for secrets or sensitive personal data, and restrict access to logs.

Risk: The Baidu API key is loaded from BAIDU_API_KEY or a .env file.

Mitigation: Protect the .env file and use standard secret-handling practices for local and shared environments.

Risk: Dependency installation may vary across environments.

Mitigation: Prefer a locked dependency install before shared or production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yky3489/skills/openclaw-cn)
- [Baidu AI Search documentation](https://cloud.baidu.com/doc/WENXINWORKSHOP/s/2m0u2qdmd)
- [Baidu Qianfan application console](https://console.bce.baidu.com/qianfan/ais/console/applicationConsole/application)
- [Baidu Qianfan web search endpoint](https://qianfan.baidubce.com/v2/ai_search/web_search)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration]

**Output Format:** [Markdown guidance and JSON search-result payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results include title, URL, snippet, site name, and total result count.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact SKILL.md frontmatter reports 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
