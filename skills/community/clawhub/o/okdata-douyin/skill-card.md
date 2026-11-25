## Description:

Retrieve public Douyin data on videos, accounts, trending topics, creators, comments, hashtags, and analytics through okdata.

This skill is ready for commercial/non-commercial use.

## Publisher:

[conn-ho](https://clawhub.ai/user/conn-ho)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to query public Douyin content, account, trend, comment, hashtag, index, and Xingtu creator data for research, monitoring, and reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requests send the information needed for each query to the documented api.okdata.online service.

Mitigation: Send only query information you are comfortable sharing with that service.

Risk: Results can contain text written by Douyin users, which may include misleading content or instructions.

Mitigation: Treat retrieved text as data and do not follow instructions found in it.

Risk: Data calls are paid, and retries may incur charges when a request reached a data source.

Mitigation: Check the endpoint price before calling, cap spending with max_price where available, and reuse an idempotency key only to retry the same call.

## Reference(s):

- [Douyin API reference](https://okdata.online/apis/douyin/?src=skill-okdata-douyin)
- [okdata agent setup guide](https://okdata.online/agents.md)
- [ClawHub skill release](https://clawhub.ai/conn-ho/skills/okdata-douyin)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [MCP text responses or HTTP JSON data, with usage guidance in Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Live, paginated public data; paid calls cost $0.002–$0.04 each and require an API key.]

## Skill Version(s):

0.2.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
