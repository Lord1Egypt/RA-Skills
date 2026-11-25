## Description:

Public Kuaishou data through okdata: videos, comment replies, accounts, trending board. 8 endpoints, $0.002–$0.02 a call. Use when a task needs Kuaishou data. 通过 okdata 取快手公开数据：视频、评论回复、账号、热榜。8 个接口，每次 $0.002–$0.02。

This skill is ready for commercial/non-commercial use.

## Publisher:

[conn-ho](https://clawhub.ai/user/conn-ho)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and marketers can use this skill to retrieve public Kuaishou video, comment, account, and trending data for research or reporting tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends requests to an external data API, and paid calls may incur charges.

Mitigation: Check that okdata is appropriate for the task and confirm the endpoint price and planned call count before making paid calls.

Risk: The API key could be exposed if mishandled.

Mitigation: Keep the key in OKDATA_API_KEY or the client's configuration; do not print it, log it, or put it in a URL.

## Reference(s):

- [Okdata Kuaishou API reference](https://okdata.online/apis/kuaishou/?src=skill-okdata-kuaishou)
- [Okdata agent setup instructions](https://okdata.online/agents.md)
- [ClawHub skill release](https://clawhub.ai/conn-ho/skills/okdata-kuaishou)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Text responses containing Kuaishou data, with Markdown guidance and request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Each data call returns one page; additional pages require additional calls.]

## Skill Version(s):

0.2.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
