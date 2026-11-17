## Description:

Baidu Web Search starts Baidu web searches during conversations and returns summaries and link lists for questions such as finding a company website or recent policy documents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jisuapi](https://clawhub.ai/user/jisuapi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve current Baidu web search results, including titles, URLs, snippets, dates, and request IDs, for conversational answers that need fresh webpage references.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms are sent to Baidu Qianfan.

Mitigation: Avoid sensitive or private queries unless that information is appropriate to share with Baidu.

Risk: The skill depends on a Baidu AppBuilder API key stored in BAIDU_API_KEY.

Mitigation: Store the key in the environment only where the skill is intended to run and rotate it according to local credential policy.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jisuapi/skills/jisu-baidu)
- [Baidu Qianfan Web Search API documentation](https://cloud.baidu.com/doc/qianfan-api/s/Wmbq4z7e5)
- [Baidu Qianfan Web Search endpoint](https://qianfan.baidubce.com/v2/ai_search/web_search)
- [JisuAPI website](https://www.jisuapi.com/)
- [JisuEPC website](https://www.jisuepc.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [JSON search results with optional Markdown summaries and inline shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and BAIDU_API_KEY; search requests are sent to Baidu Qianfan.]

## Skill Version(s):

1.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
