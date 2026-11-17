## Description:

每日财经早报：A股行情 + RSS全球新闻聚合，自动生成Markdown简报

This skill is ready for commercial/non-commercial use.

## Publisher:

[answeryl](https://clawhub.ai/user/answeryl)

### License/Terms of Use:

MIT-0

## Use Case:

External users and finance-news readers use this skill to generate a Chinese-language daily market briefing that combines A-share index data with China News RSS headlines, categorized news summaries, source links, and a dated Markdown archive.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts China News RSS and Tencent market-data endpoints during execution.

Mitigation: Install and run it only in environments where those outbound requests are acceptable.

Risk: Market data is fetched from an HTTP endpoint and may be unavailable, stale, or modified in transit.

Mitigation: Verify market data against trusted financial sources before using it for financial decisions.

Risk: The script automatically creates and writes dated Markdown reports under the user's Desktop by default.

Mitigation: Review or change the configured output directory before scheduled or repeated execution.

Risk: The artifact requires the third-party requests dependency.

Mitigation: Install dependencies in a virtual environment with pinned versions before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/answeryl/skills/global-market-briefing)
- [ClawHub homepage metadata](https://clawhub.com/skills/global-market-briefing)
- [China News RSS](https://www.chinanews.com.cn/rss/)
- [Tencent market data endpoint](http://qt.gtimg.cn/q=sh000001,sz399001,sz399006,sh000688,sh000016)

## Skill Output:

**Output Type(s):** [text, markdown, files]

**Output Format:** [Markdown briefing saved as a dated local file, with a shorter plain-text/Markdown summary printed to stdout unless full stdout mode is requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The script writes dated reports under ~/Desktop/早间新闻 by default and can print the full Markdown report with --stdout.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
