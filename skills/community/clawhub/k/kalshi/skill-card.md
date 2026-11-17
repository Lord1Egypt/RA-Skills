## Description:

Read-only Kalshi prediction market integration for viewing markets, checking portfolio positions, analyzing prediction opportunities, and finding high-payoff/high-certainty trades.

This skill is ready for commercial/non-commercial use.

## Publisher:

[henrik-openclaw](https://clawhub.ai/user/henrik-openclaw)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to inspect Kalshi market data, review authenticated portfolio information, and generate read-only market opportunity analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Portfolio features require local Kalshi API credentials and a private key.

Mitigation: Configure credentials only when portfolio access is needed, store ~/.kalshi/credentials.json and the private key as sensitive secrets, and keep file permissions restrictive.

Risk: Opportunity analysis may be mistaken for financial advice.

Mitigation: Treat generated opportunity output as informational analysis only and independently evaluate market risk before making trading decisions.

Risk: The scripts depend on external Python packages and network API responses.

Mitigation: Install dependencies in an isolated Python environment and review or pin packages where possible.

## Reference(s):

- [Kalshi API Reference](references/api.md)
- [Kalshi API](https://api.elections.kalshi.com/trade-api/v2)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal text with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only market and portfolio output; portfolio commands require locally configured Kalshi API credentials.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
