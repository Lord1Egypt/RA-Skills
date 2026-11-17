## Description: <br>
新闻聚合工具免费版 helps an agent search supported Chinese news sources, filter duplicates and lower-confidence items, and produce structured technology, military, and society news summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, students, and developers use this skill to request lightweight daily or recent news briefings across supported domestic technology, military, and society sources. The agent searches available sources, filters duplicates and low-confidence items, and returns categorized summaries with source context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may prompt an agent to make live web or search requests to news sources. <br>
Mitigation: Use it only where outbound web access is acceptable, and review cited sources before relying on the generated summary. <br>
Risk: A callback URL can send results to an external destination if supplied. <br>
Mitigation: Provide callback_url only when result delivery is intended and the destination is trusted. <br>
Risk: News summaries can be incomplete, duplicated, outdated, or based on low-confidence reports. <br>
Mitigation: Prefer official or authoritative sources, retain source and time context in outputs, and verify important claims before reuse. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/news-aggregator-tool-free) <br>
- [36Kr technology channel](https://36kr.com/information/tech/) <br>
- [Machine Heart](https://www.jiqizhixin.com/) <br>
- [Tencent military news](https://new.qq.com/om/mil/) <br>
- [CCTV News](http://news.cctv.com/) <br>
- [Xinhua News](http://www.xinhuanet.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown news summaries with optional inline shell commands and YAML configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Summaries may include category headings, item titles, sources, timestamps, key points, credibility filtering, and deduplication notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
