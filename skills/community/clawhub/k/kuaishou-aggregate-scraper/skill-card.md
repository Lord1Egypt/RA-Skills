## Description: <br>
快手全场景数据查询助手。支持App和Web双端API，覆盖视频详情、用户数据、搜索、热榜、直播、评论等全功能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[new-ironman](https://clawhub.ai/user/new-ironman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, content operators, product teams, and developers use this skill to query Kuaishou video, user, search, trending, live, and comment data through MaxHub APIs and turn the results into concise analysis or reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends Kuaishou identifiers, links, search terms, and related profile or video data to MaxHub at aconfig.cn. <br>
Mitigation: Use the skill only when that data sharing is intended, and avoid submitting sensitive or unnecessary personal data. <br>
Risk: The skill requires MAXHUB_API_KEY, a sensitive credential. <br>
Mitigation: Store the key in a secret manager or local environment, keep it out of shared repositories and logs, and rotate it if exposure is suspected. <br>
Risk: Security evidence reports unexpected cross-platform fallback routes that do not match the Kuaishou-only description. <br>
Mitigation: Review endpoint paths before use and prefer the documented Kuaishou API references when running or modifying the skill. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/new-ironman/kuaishou-aggregate-scraper) <br>
- [MaxHub API Website](https://www.aconfig.cn) <br>
- [Video & Content API](references/api-video.md) <br>
- [User Data API](references/api-user.md) <br>
- [Parameter Mappings](references/param-mappings.md) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Markdown, Shell commands, Guidance, Analysis] <br>
**Output Format:** [Markdown with tables, bullet points, links, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Output language follows the user's language; API key values must not be exposed.] <br>

## Skill Version(s): <br>
3.6.1 (source: server release metadata, skill metadata, and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
