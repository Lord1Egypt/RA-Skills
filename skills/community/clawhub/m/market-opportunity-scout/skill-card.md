## Description:

市场机会侦察兵 - 自动监控 A/H 股市场异动、财经新闻、热点板块，生成投资机会简报。适合投资者、交易员、金融从业者。

This skill is for research and development only.

## Publisher:

[yoriko233](https://clawhub.ai/user/yoriko233)

### License/Terms of Use:

MIT-0

## Use Case:

Investors, traders, and finance professionals use this skill to generate A/H-share market opportunity briefings that summarize index movement, hot sectors, unusual stocks, finance news, and opportunity notes. Its outputs should be treated as research support rather than investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill presents current-dated market claims that may be hard-coded or stale, which can be mistaken for live investment signals.

Mitigation: Verify all market data, timestamps, and news items against reliable live sources before using the report for decisions.

Risk: Live data parsing, source timestamps, failure handling, and dependency pinning are not established in the evidence.

Mitigation: Add explicit source timestamps, visible fetch failures, and pinned dependencies before relying on the skill in a workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yoriko233/skills/market-opportunity-scout)
- [Eastmoney quote API - Shanghai Composite](https://push2.eastmoney.com/api/qt/stock/get?secid=1.000001&fields=f43,f44,f170)
- [Eastmoney quote API - Hang Seng Index](https://push2.eastmoney.com/api/qt/stock/get?secid=100.HSI&fields=f43,f44,f170)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown market briefing with command examples and JSON configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports can be generated in daily, stock, or sector modes; market values should be treated as delayed or sample data unless independently verified.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
