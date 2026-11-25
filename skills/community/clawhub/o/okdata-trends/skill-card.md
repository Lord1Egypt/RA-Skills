## Description:

What is trending right now? Reads the trending board of every platform you pick, one call each, as one table with a platform column: rank, topic and heat. Use when the user asks this about Douyin, Xiaohongshu (RedNote), Bilibili, Weibo, X (Twitter), Reddit, Kuaishou. 此刻各平台在热什么？读你选的每个平台的热榜，每个平台一次调用，排成一张带平台列的表：排名、话题和热度。

This skill is ready for commercial/non-commercial use.

## Publisher:

[conn-ho](https://clawhub.ai/user/conn-ho)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to compare current trending topics and reported heat across selected social platforms in one table. It fetches one board for each selected platform through okdata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requests to okdata.online require trust in that service and can incur per-call charges.

Mitigation: Review the selected platforms and stated maximum cost before fetching, and keep the API key in the approved client configuration.

Risk: The security review had partial coverage because several local references could not be resolved.

Mitigation: Review the unresolved references and verify the skill and okdata.online service before installing.

## Reference(s):

- [okdata trends skill documentation (English)](https://okdata.online/skills/trends/?src=skill-okdata-trends)
- [okdata trends skill documentation (中文)](https://okdata.online/zh/skills/trends/?src=skill-okdata-trends)

## Skill Output:

**Output Type(s):** [API Calls, Markdown, Guidance]

**Output Format:** [Markdown table with platform, rank, topic, heat, and link, followed by cost and source details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One board call per selected platform; leave unavailable figures blank rather than guessing.]

## Skill Version(s):

0.2.3 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
