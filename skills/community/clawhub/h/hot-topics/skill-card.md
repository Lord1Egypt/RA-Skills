## Description: <br>
Get real-time trending topics and hot searches from major Chinese social media platforms including Weibo, Zhihu, Baidu, Douyin, Toutiao, and Bilibili. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[NeverChenX](https://clawhub.ai/user/NeverChenX) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to retrieve and summarize current trending topics from major Chinese social media, search, video, and news platforms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Requests for ambiguous trend information may be sent to a third-party API with unnecessary private, client, or business context. <br>
Mitigation: Specify the intended Chinese platform or region and avoid including sensitive interests, client names, or confidential business context in trend requests. <br>
Risk: Trend results depend on a third-party service and may be delayed, unavailable, or cached. <br>
Mitigation: Handle network errors, check timestamps when present, and cache or retry results according to the skill guidance. <br>


## Reference(s): <br>
- [60s API Documentation](https://docs.60s-api.viki.moe) <br>
- [60s API Base Endpoint](https://60s.viki.moe/v2) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown with JSON, Python, and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns ranked trend data and summaries from third-party API responses; no API key is required.] <br>

## Skill Version(s): <br>
1.1.0 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
