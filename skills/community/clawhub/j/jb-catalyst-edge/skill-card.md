## Description:

Identifies high-conviction stock opportunities and tracks a retirement portfolio with weekly scans, quarterly reviews, and FIRE signal analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[j3m2b](https://clawhub.ai/user/j3m2b)

### License/Terms of Use:

MIT-0

## Use Case:

Agents supporting the publisher's finance workflow use this skill to scan a small stock watchlist, produce RSI-based buy/sell/hold signals, and maintain retirement/FIRE planning summaries. It is intended for weekly monitoring, quarterly portfolio review, and concise Discord-ready financial updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package includes real personal and household financial records.

Mitigation: Remove or replace private financial records before installation, distribution, or agent use.

Risk: The package includes an exposed Alpha Vantage key.

Mitigation: Rotate the key and require secrets to be supplied through a secure runtime configuration.

Risk: The skill can post financial summaries to a fixed Discord destination without clear confirmation controls.

Mitigation: Make delivery opt-in, show a payload preview, and require destination verification before sending.

Risk: The skill references broad memory access for personal context.

Mitigation: Limit memory reads to the minimum necessary files and require user approval before including private context in reports.

## Reference(s):

- [Catalyst Edge on ClawHub](https://clawhub.ai/j3m2b/skills/jb-catalyst-edge)
- [Publisher profile](https://clawhub.ai/user/j3m2b)
- [Yahoo Finance chart API endpoint](https://query1.finance.yahoo.com/v8/finance/chart/)
- [Alpha Vantage query endpoint](https://www.alphavantage.co/query)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, JSON scan results, Discord-ready alert payloads, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs can include dated market data, ticker scores, local file updates, and financial planning notes that require human review before use.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
