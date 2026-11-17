## Description:

Provides Chinese A-share market sentiment and sector rise/fall summaries using Niuguwang public market-data endpoints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lbl581581](https://clawhub.ai/user/lbl581581)

### License/Terms of Use:

MIT-0

## Use Case:

Investors, analysts, and market watchers can ask an agent to summarize current A-share market sentiment, sector strength, and sector weakness as informational decision-support context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Market sentiment summaries could be mistaken for financial advice.

Mitigation: Present the data as informational context only and avoid directing specific investment actions.

Risk: The skill depends on public Niuguwang market-data endpoints for current values.

Mitigation: Check returned timestamps and values before relying on a response, and disclose the data source.

Risk: The skill requires a promotional footer with an external app/download link.

Mitigation: Confirm the footer is acceptable for the deployment context and keep the source/link clearly separated from analysis.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lbl581581/skills/ngw-market-sentiment)
- [Niuguwang market emotion endpoint](https://stq.niuguwang.com/taoquant/DBXF/GetMarketEmotion?plateType=-1)
- [Niuguwang plate emotion ranking endpoint](https://stq.niuguwang.com/taoquant/DBXF/GetPlateEmoRank)
- [StockHN app download page](https://www.stockhn.com/#/appDownload)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown text with optional shell command examples and sourced footer]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses should treat market data as informational and append the disclosed source footer when the skill is used.]

## Skill Version(s):

1.0.1 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
