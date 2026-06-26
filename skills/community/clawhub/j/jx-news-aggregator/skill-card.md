## Description: <br>
国内外社会、科技、军事新闻汇总。自动搜索、筛选、整理新闻要点。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kirkraman](https://clawhub.ai/user/kirkraman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers use this skill to search Chinese and international social, technology, and military news, filter duplicate or unreliable results, and produce categorized briefings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: News queries and returned snippets are sent to SkillBoss. <br>
Mitigation: Avoid private, confidential, or regulated topics unless SkillBoss is approved for that use. <br>
Risk: The skill requires a sensitive API credential. <br>
Mitigation: Use a scoped or revocable SKILLBOSS_API_KEY and rotate it if exposure is suspected. <br>
Risk: Aggregated news can include duplicate, stale, anonymous, or secondhand reports. <br>
Mitigation: Prioritize official media and authoritative institutions, and treat forum posts, anonymous claims, and reposts cautiously. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kirkraman/jx-news-aggregator) <br>
- [SkillBoss API Hub](https://api.skillbossai.com/v1) <br>
- [36Kr Technology News](https://36kr.com/information/tech/) <br>
- [Jiqizhixin](https://www.jiqizhixin.com/) <br>
- [ITHome](https://www.ithome.com/) <br>
- [Guancha](https://www.guancha.cn/) <br>
- [The Paper](https://www.thepaper.cn/) <br>
- [Tencent Military](https://new.qq.com/om/mil/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Structured Markdown news summary with categorized links, sources, timestamps, and key points.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY and uses SkillBoss API Hub search and chat requests.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
