## Description:

Public YouTube data through okdata: videos, comment replies, channels, posts. 10 endpoints, $0.002–$0.004 a call. Use when a task needs YouTube data. 通过 okdata 取YouTube公开数据：视频、评论回复、channels、帖子。10 个接口，每次 $0.002–$0.004。

This skill is ready for commercial/non-commercial use.

## Publisher:

[conn-ho](https://clawhub.ai/user/conn-ho)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use the skill to retrieve public YouTube video, comment, transcript, channel, and post data for research and content analysis tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requests may send search terms or other supplied information to the external okdata API.

Mitigation: Before calling the API, check that the information included in the request is appropriate to send to that service.

Risk: API calls are paid, and fetching additional pages incurs additional calls.

Mitigation: Before the first paid call, state the planned endpoint and maximum cost; request more pages only when needed.

## Reference(s):

- [okdata YouTube API reference](https://okdata.online/apis/youtube/?src=skill-okdata-youtube)
- [okdata agent setup guide](https://okdata.online/agents.md)

## Skill Output:

**Output Type(s):** [Text, API Calls, Shell commands, Guidance]

**Output Format:** [Text responses, with JSON request examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returned data is paginated; additional pages require separate calls.]

## Skill Version(s):

0.2.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
