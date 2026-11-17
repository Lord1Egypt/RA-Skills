## Description:

Fetches trending topics from multiple public platforms and analyzes likely positive or negative effects on rates, credit, Shenwan industries, related securities, and futures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bianchunhui](https://clawhub.ai/user/bianchunhui)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and market analysts use Hot Analyzer to collect public trending-topic data, merge duplicate events, rank finance-relevant signals, and draft market-impact analysis for bonds, industries, securities, and futures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes public web requests to trending-topic APIs that may be unavailable, incomplete, rate-limited, or structurally changed.

Mitigation: Review the fetched raw JSON and generated rankings before relying on the report.

Risk: The workflow creates or overwrites several files in the working directory.

Mitigation: Run the skill in a new empty folder and inspect generated paths before execution.

Risk: Generated market analysis can be time-sensitive, incomplete, or misleading if treated as investment advice.

Mitigation: Use the analysis as informational context only and verify conclusions against current market data and professional judgment.

## Reference(s):

- [Hot Analyzer on ClawHub](https://clawhub.ai/bianchunhui/skills/hot-analyzer)
- [Toutiao Hot Board](https://www.toutiao.com/hot-event/hot-board/?origin=toutiao_pc)
- [Baidu Realtime Hot Board](https://top.baidu.com/api/board?tab=realtime)
- [Weibo Hot Search](https://weibo.com/ajax/side/hotSearch)
- [Douyin Hot Search](https://www.iesdouyin.com/web/api/v2/hotsearch/billboard/word/)
- [Zhihu Hot Topics](https://www.zhihu.com/hot)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown report with shell commands, JSON intermediate files, and an HTML report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates working-directory files including raw platform JSON captures, state.json, pending.json, groups.json, compute.py, and hot_analysis_report.html.]

## Skill Version(s):

1.0.1 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
