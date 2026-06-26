## Description: <br>
市场洞察师 helps agents monitor online fiction platform policies, collect public ranking snapshots, analyze market trends, and produce opportunity and competitor reports for publishing decisions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ouyang198000](https://clawhub.ai/user/ouyang198000) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content strategists, publishing teams, and agent workflows use this skill to track public rankings, platform policy changes, competitor signals, and emerging online-fiction market opportunities. It is intended to support topic selection and market reports with source, timestamp, and confidence labels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Data-collection guidance may be read as encouraging proxy, bypass, or cookie-based scraping that conflicts with platform rules. <br>
Mitigation: Use only public rankings, official APIs, licensed datasets, or first-party authorized accounts, and do not supply cookies, session tokens, or proxy pools. <br>
Risk: Market reports can overstate confidence when source data is incomplete or time-sensitive. <br>
Mitigation: Label each report with source, collection time, freshness, confidence, and known gaps before using recommendations for decisions. <br>


## Reference(s): <br>
- [平台详解参考](references/platform-guide.md) <br>
- [ClawHub skill page](https://clawhub.ai/ouyang198000/market-insight-agent) <br>
- [Amazon Kindle Store Best Sellers](https://www.amazon.com/gp/bestsellers/digital-text/) <br>
- [起点中文网排行榜](https://www.qidian.com/rank/) <br>
- [番茄小说排行榜](https://fanqienovel.com/rank/) <br>
- [Royal Road Best Rated](https://www.royalroad.com/fictions/best-rated) <br>
- [Wattpad Popular Stories](https://www.wattpad.com/stories/popular) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [JSON data snapshots and Markdown market reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports should include data source, collection time, freshness notes, confidence rating, and known limitations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
