## Description:

Uses Eastmoney MX to turn natural-language A-share and market-universe screening requests into condition-based stock-screening queries, CSV exports, and concise result summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zoeluli7459-dev](https://clawhub.ai/user/zoeluli7459-dev)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to screen A-share stocks, listed companies, sectors, indexes, boards, and concepts by market, valuation, financial, industry, and ranking constraints. It is intended for data-screening candidates and constituent lookup, not single-security quote lookup, news research, watchlist management, simulated trading, or personalized buy/sell advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Screening queries and an MX API key are sent to Eastmoney.

Mitigation: Install only when that data sharing is acceptable, keep the API key in MX_APIKEY, and avoid placing secrets in prompts or generated files.

Risk: Generated CSV, description, and raw JSON files can reveal local records of screening activity.

Mitigation: Store outputs in an appropriate MX_OUTPUT_DIR, review files before sharing, and delete generated records that are no longer needed.

Risk: CSV values from the API are written without neutralizing formula-like content.

Mitigation: Inspect CSVs before opening them in spreadsheet applications and use a safer viewer or sanitization step for untrusted rows.

Risk: Screening results may be mistaken for investment recommendations.

Mitigation: Present matches as data-screening candidates and preserve the skill boundary against personalized buy/sell advice unless separately reviewed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zoeluli7459-dev/skills/mx-xuangu)
- [Result Fields Reference](artifact/references/result-fields.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Files, Configuration guidance]

**Output Format:** [Markdown summary with inline shell commands plus generated CSV, description text, and raw JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MX_APIKEY and may use MX_OUTPUT_DIR to choose where generated files are written.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
