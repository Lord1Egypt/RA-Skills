## Description:

Tracks recent IPOs and generates TradingView watchlists from IPO calendar and market data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sarkcesscrewpay](https://clawhub.ai/user/sarkcesscrewpay)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to fetch recent IPO information, enrich listings with market data, and produce TradingView watchlists plus report and CSV outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may run Python commands, install dependencies, fetch market data from external services, and write IPO report or watchlist files.

Mitigation: Review the actual script, dependency file, command options, and output paths before execution.

Risk: The inspected artifact does not include the referenced script or dependency files.

Mitigation: Confirm those files are present and trustworthy before running the skill.

Risk: IPO and market data can be incomplete, stale, or unsuitable for trading decisions.

Mitigation: Review generated reports and watchlists against authoritative market sources before importing or acting on them.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance with shell commands and generated TXT/CSV files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces ipo_watchlist.txt, ipo_report.txt, and ipo_data.csv when the referenced IPO tracker script is available.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
