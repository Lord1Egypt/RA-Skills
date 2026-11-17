## Description:

Generates Chinese-language investment committee reports by combining market data, fundamental context, and five investor-style analytical frameworks for stocks, ETFs, crypto assets, gold, and commodities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bitwater](https://clawhub.ai/user/bitwater)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to analyze buy decisions, position management, and comparisons across public market assets. It produces a committee-style report with scores, rationale, risk notes, position guidance, stop-loss conditions, and a final verdict.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish and store sensitive investment reports.

Mitigation: Do not provide sensitive account details or private portfolio information unless the runtime requires explicit confirmation before sharing or storing the report.

Risk: The skill gives specific trade guidance, including position sizing, stop-losses, and target prices.

Mitigation: Treat generated guidance as educational analysis rather than personalized financial advice, and review decisions independently before acting.

Risk: The skill performs market-data and web lookups that may affect report accuracy.

Mitigation: Review source freshness and key data points before relying on generated conclusions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bitwater/skills/investment-committee)
- [stooq.com market data endpoint](https://stooq.com/q/d/l/?s={sym}&d1={d1}&d2={d2}&i=d)
- [Report Template](assets/report-template.md)
- [Stanley Druckenmiller Framework](references/druckenmiller.md)
- [Duan Yongping Framework](references/duan.md)
- [Howard Marks Framework](references/marks.md)
- [Charlie Munger Framework](references/munger.md)
- [James Simons Framework](references/simons.md)
- [Committee Verdict Rules](references/verdict.md)

## Skill Output:

**Output Type(s):** [analysis, markdown, shell commands, guidance]

**Output Format:** [Markdown investment report in Chinese, with optional shell command output used as supporting market data.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include specific scores, position sizing, stop-loss levels, target prices, report archives, and Discord channel posting.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
