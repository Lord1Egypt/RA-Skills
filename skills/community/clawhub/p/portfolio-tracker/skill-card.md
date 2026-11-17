## Description:

Automates live portfolio tracking and analysis using browser automation on Yahoo Finance for Vish's stocks, ETFs, and crypto holdings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vachanalaviswanath](https://clawhub.ai/user/vachanalaviswanath)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to update and analyze a specific stock, ETF, and crypto portfolio with live Yahoo Finance data, including performance summaries, winners and losers, and rebalancing suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Personal holdings and ticker lookup activity may be exposed through Yahoo Finance browsing and the configured Chrome profile.

Mitigation: Use the skill only for intended portfolio updates, choose an appropriate browser profile, and account for what the browsing session may reveal.

Risk: Broad trigger wording could lead to local financial record updates during general market or investment requests.

Mitigation: Confirm update intent before writing portfolio-tracker.md and review proposed changes before applying them.

## Reference(s):

- [Portfolio Holdings Reference](references/portfolio-holdings.md)
- [Portfolio Tracker ClawHub Page](https://clawhub.ai/vachanalaviswanath/skills/portfolio-tracker)
- [Yahoo Finance Quote Pages](https://finance.yahoo.com/quote/BTC-USD)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown analysis with portfolio tables, browser workflow steps, and optional Python helper output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the configured Chrome profile and local holdings file as inputs; proposed portfolio record updates should be reviewed before writing.]

## Skill Version(s):

0.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
