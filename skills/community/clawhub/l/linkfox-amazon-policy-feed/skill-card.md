## Description:

查询亚马逊最新政策法规与资讯，支持按站点和时间区间分页检索含 AI 中文摘要的列表，并按记录 ID 获取完整正文。

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, operators, and agents use this skill to retrieve Amazon seller policy and compliance update lists, review Chinese summaries, and fetch the full article body for selected feed records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles account login, API keys, and billing flows.

Mitigation: Use the official LinkFox website for API key setup when possible, do not provide SMS codes unless registration or login is intended, and confirm paid orders outside the agent flow.

Risk: The skill can persist full API responses and submit feedback automatically.

Mitigation: Review local response storage and feedback behavior before use, especially when policy queries or returned content may be sensitive.

Risk: Custom LINKFOX_* API origin variables can redirect requests away from the default service endpoints.

Mitigation: Avoid custom LinkFox endpoint environment variables unless the destination is trusted and expected.

## Reference(s):

- [API Reference](references/api.md)
- [Authentication and Billing Onboarding](references/onboarding.md)
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/skills/linkfox-amazon-policy-feed)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [JSON feed records and Markdown article detail, summarized or rendered by the agent]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Full responses are saved locally; large responses are summarized unless inline output is requested.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
