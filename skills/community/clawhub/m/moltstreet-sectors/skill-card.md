## Description:

AI signals for 11 SPDR sector ETFs, sector rotation, and industry analysis with multi-analyst debate. Free, no API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fredxyt](https://clawhub.ai/user/fredxyt)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to fetch MoltStreet sector ETF analysis and summarize rotation, bullish or bearish consensus, confidence, and sector comparisons for the 11 SPDR sector ETFs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sector ETF requests are fetched from MoltStreet public endpoints.

Mitigation: Install only when this data sharing is acceptable, and avoid submitting sensitive portfolio information in requests.

Risk: The returned market analysis is AI-generated and informational, not financial advice.

Mitigation: Present outputs as informational, verify important claims against authoritative market data, and do not rely on the response alone for trading decisions.

Risk: The skill documentation says analysis updates multiple times daily and is not real-time quotes.

Mitigation: Use real-time market data sources when current prices or execution-sensitive decisions are required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fredxyt/skills/moltstreet-sectors)
- [MoltStreet homepage](https://moltstreet.com)
- [MoltStreet skill documentation](https://moltstreet.com/skill.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands and summarized sector analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses public MoltStreet endpoints via curl; no API key required.]

## Skill Version(s):

1.0.1 (source: server release, manifest.json, skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
