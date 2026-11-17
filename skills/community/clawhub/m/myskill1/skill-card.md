## Description:

Fetches U.S. 10-year Treasury yield data from CNBC and Treasury.gov, writes it to a CSV file, and appends a concise run log.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kid0114](https://clawhub.ai/user/kid0114)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to retrieve current U.S. 10-year Treasury yield data, compare CNBC and Treasury.gov values, and maintain a local CSV history with a simple execution log.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes outbound requests to CNBC and Treasury.gov.

Mitigation: Install only in environments where access to those public data sources is acceptable.

Risk: The skill creates or updates a local CSV file and appends a local fetch log.

Mitigation: Review the output paths before execution and run it in a workspace where those file writes are expected.

Risk: The skill instructions and console output are primarily in Chinese.

Mitigation: Non-Chinese readers should translate the instructions before relying on operational details.

Risk: The activation phrase `fetch treasury` is broader than the slash command.

Mitigation: Prefer `/us-treasury-tracker` when stricter activation is desired.

## Reference(s):

- [CNBC US10Y quote](https://www.cnbc.com/quotes/US10Y)
- [Treasury.gov daily Treasury yield curve data](https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve&field_tdr_date_value=2026)

## Skill Output:

**Output Type(s):** [text, shell commands, files]

**Output Format:** [Markdown guidance with shell command examples; generated CSV and log files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates testdata/us_treasury_10y.csv and appends skills/us-treasury-tracker/logs/fetch.log.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
