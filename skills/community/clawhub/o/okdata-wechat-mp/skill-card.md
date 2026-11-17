## Description:

Public WeChat Official Accounts data through okdata: accounts, articles, comment replies. 8 endpoints, $0.02–$0.15 a call. Use when a task needs WeChat Official Accounts data. 通过 okdata 取微信公众号公开数据：账号、文章、评论回复。8 个接口，每次 $0.02–$0.15。

This skill is ready for commercial/non-commercial use.

## Publisher:

[conn-ho](https://clawhub.ai/user/conn-ho)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts can use this skill to retrieve public WeChat Official Account profiles, articles, engagement metrics, ownership details, comments, and replies through okdata for research and reporting tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends requests to the external okdata API, and calls may incur charges.

Mitigation: Review the endpoint and maximum cost before each paid call, and keep OKDATA_API_KEY out of prompts, URLs, and logs.

## Reference(s):

- [WeChat Official Accounts API reference](https://okdata.online/apis/wechat_mp/?src=skill-okdata-wechat-mp)
- [okdata agent setup guide](https://okdata.online/agents.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Text or Markdown responses with WeChat Official Account data and source details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may be paginated; additional pages require separate API calls.]

## Skill Version(s):

0.2.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
