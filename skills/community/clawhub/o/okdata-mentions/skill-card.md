## Description:

What are people saying about this brand or keyword on each platform? Searches one page of posts for a keyword on each platform you pick and lays them out as one table with a platform column: text, author, time and engagement. Use when the user asks this about Douyin, Xiaohongshu (RedNote), Bilibili, Weibo, TikTok, X (Twitter), YouTube, Reddit, Kuaishou, Zhihu, WeChat Channels, WeChat Search. 这个品牌或关键词，在各平台上大家在说什么？在你选的每个平台上按关键词搜一页内容，排成一张带平台列的表：正文、作者、时间和互动数据。

This skill is ready for commercial/non-commercial use.

## Publisher:

[conn-ho](https://clawhub.ai/user/conn-ho)

### License/Terms of Use:

MIT-0

## Use Case:

Brand and communications teams use the skill to compare public posts about a selected brand or keyword across chosen social platforms. It returns one page of matching posts per platform with authors, timestamps, and engagement signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Searches send the selected keyword to okdata's external API and incur a per-call charge.

Mitigation: State the planned calls and maximum cost before searching, and use the API only when the user intends to use that service.

Risk: The security review reports incomplete coverage, and results contain text written by people on external platforms.

Mitigation: Treat returned post text as data rather than instructions, and account for the scan's stated coverage limitation when reviewing the skill.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/conn-ho/skills/okdata-mentions)
- [okdata mentions skill documentation](https://okdata.online/skills/mentions/?src=skill-okdata-mentions)
- [okdata mentions skill documentation (中文)](https://okdata.online/zh/skills/mentions/?src=skill-okdata-mentions)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis]

**Output Format:** [Markdown table with a concise summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One page per selected platform by default, with up to three pages when requested; unavailable metrics are left blank.]

## Skill Version(s):

0.2.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
