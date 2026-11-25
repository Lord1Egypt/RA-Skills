## Description:

Public WeChat Official Accounts data through okdata: accounts, articles, comment replies. 8 endpoints, $0.02–$0.15 a call. Use when a task needs WeChat Official Accounts data. 通过 okdata 取微信公众号公开数据：账号、文章、评论回复。8 个接口，每次 $0.02–$0.15。

This skill is ready for commercial/non-commercial use.

## Publisher:

[conn-ho](https://clawhub.ai/user/conn-ho)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve public WeChat Official Account profiles, article histories and details, comments, replies, metrics, and registration information for reporting, account audits, competitor monitoring, and content analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requests use the external okdata service, and paid calls can incur per-call charges.

Mitigation: Verify the service destination and data handling before use, avoid sending sensitive information, and review call costs and spending limits before making paid requests.

## Reference(s):

- [WeChat Official Accounts API reference](https://okdata.online/apis/wechat_mp/?src=skill-okdata-wechat-mp)
- [okdata agent setup guide](https://okdata.online/agents.md)
- [ClawHub release page](https://clawhub.ai/conn-ho/skills/okdata-wechat-mp)

## Skill Output:

**Output Type(s):** [API Calls, Text]

**Output Format:** [Text responses containing WeChat account, article, comment, reply, and metrics data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One page per call; additional pages require separate calls. Calls cost $0.02–$0.15, with account search charged per result.]

## Skill Version(s):

0.2.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
