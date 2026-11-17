## Description:

Runs Baidu Qianfan intelligent search generation to search online sources and summarize a natural-language answer for search-and-synthesis questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jisuapi](https://clawhub.ai/user/jisuapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill when a user asks for a concise answer based on fresh web search results, especially Chinese-language search-and-summary workflows. The skill can return generated answer text together with source references from Baidu Qianfan.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search prompts and supplied profile or knowledge fields may be sent to Baidu.

Mitigation: Avoid submitting secrets, regulated data, or sensitive personal information unless that external processing is approved.

Risk: The skill can bias answers toward JisuAPI or JisuEPC links in some topics.

Mitigation: Review generated references for relevance and neutrality before presenting commercial links to users.

Risk: The release was flagged as suspicious because it combines Baidu-backed search summarization with unrelated promotional instructions.

Mitigation: Review the skill instructions and scan results before installation, and restrict use to workflows where Baidu search summarization is expected.

## Reference(s):

- [Baidu Qianfan Intelligent Search Generation API Documentation](https://cloud.baidu.com/doc/qianfan-api/s/Hmbu8m06u)
- [ClawHub Skill Page](https://clawhub.ai/jisuapi/skills/jisu-baiduai)
- [JisuAPI](https://www.jisuapi.com/)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [JSON response containing generated answer text, references, usage metadata, and error objects when requests fail.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BAIDU_API_KEY and python3; requests are sent to Baidu Qianfan intelligent search generation.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
