## Description:

全球网络文学市场洞察智能体，用于分析网文市场趋势、调研平台政策、监控竞品数据、支持选题决策，并识别蓝海细分市场和新兴题材机会。

This skill is ready for commercial/non-commercial use.

## Publisher:

[ouyang198000](https://clawhub.ai/user/ouyang198000)

### License/Terms of Use:

MIT-0

## Use Case:

Writers, editors, and market analysts use this skill to monitor web-novel platform policies, collect public ranking signals, analyze competitor performance, and produce JSON or Markdown market reports for topic planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Collection guidance may lead users toward proxies, cookies, shared sessions, login bypasses, or anti-scraping workarounds.

Mitigation: Use only public data or official APIs, avoid proxy rotation and borrowed credentials, and confirm each target platform permits the planned collection.

Risk: Collector runs write local JSON outputs and may be pointed at unapproved folders or domains.

Mitigation: Restrict runs to approved domains and local output directories before execution.

Risk: Market reports can overstate confidence when data is sparse, stale, or drawn from a single platform.

Mitigation: Require source, collection time, freshness notes, confidence level, limitations, and assumptions in every report.

## Reference(s):

- [平台详解参考](artifact/references/platform-guide.md)
- [ClawHub skill page](https://clawhub.ai/ouyang198000/skills/market-insight-agent)
- [Amazon Kindle best sellers](https://www.amazon.com/gp/bestsellers/digital-text/)
- [起点中文网排行榜](https://www.qidian.com/rank/)
- [番茄小说排行榜](https://fanqienovel.com/rank/)
- [Royal Road best rated](https://www.royalroad.com/fictions/best-rated)
- [Wattpad popular stories](https://www.wattpad.com/stories/popular)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, JSON data snapshots, shell command examples, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports should include data source, collection time, freshness notes, confidence level, limitations, and assumptions.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
