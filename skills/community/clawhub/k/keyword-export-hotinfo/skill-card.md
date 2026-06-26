## Description: <br>
当用户需要热点盘点、指定话题爆款挖掘、跨平台热度对比、选题推荐或话题关键词聚合时使用；限定公众号、抖音、小红书三平台，按 workflow 完成关键词提取、搜索、数据校验与关键词聚合。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[if530770](https://clawhub.ai/user/if530770) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content operators, marketers, planners, and MCN researchers use this skill to inspect public-topic momentum, mine viral content patterns, compare signals across WeChat public accounts, Douyin, and Xiaohongshu, and produce keyword or angle recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Trend, interaction, and freshness outputs may be directional when source links, timestamps, or platform data are incomplete. <br>
Mitigation: Require links and timestamps when available, preserve confidence labels, and manually verify important metrics before using them for business decisions. <br>
Risk: Search results can drift outside the intended platform scope. <br>
Mitigation: Limit analysis to 公众号、抖音、小红书 and exclude other platforms even when they appear in search results. <br>
Risk: Exact engagement counts or publication dates may be missing from public snippets. <br>
Mitigation: Avoid fabricating precise numbers or dates; state that data is unavailable and suggest follow-up verification. <br>


## Reference(s): <br>
- [Core Workflow](references/core_workflow.md) <br>
- [Platform Standards](references/platform-standards.md) <br>
- [Keyword Extraction Guide](references/keyword-extraction-guide.md) <br>
- [Data Confidence](references/data-confidence.md) <br>
- [Angle Mining Guide](references/angle-mining-guide.md) <br>
- [ClawHub skill page](https://clawhub.ai/if530770/keyword-export-hotinfo) <br>
- [Publisher profile](https://clawhub.ai/user/if530770) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Structured Markdown summaries, tables, keyword lists, platform comparisons, and topic-angle recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should identify platform scope, timestamps or freshness when available, confidence labels, and unavailable data rather than fabricating links or interaction counts.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
