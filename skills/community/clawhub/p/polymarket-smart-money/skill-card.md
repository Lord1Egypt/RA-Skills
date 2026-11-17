## Description:

Discover, analyze, and filter Polymarket wallets to identify profitable traders, flag likely market makers or HFT bots, and assess copy-trading reliability.

This skill is ready for commercial/non-commercial use.

## Publisher:

[griffithkk3-del](https://clawhub.ai/user/griffithkk3-del)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to find and evaluate Polymarket wallets for smart-money discovery, market-maker and HFT filtering, and copy-trading reliability assessment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to run code and activate a virtual environment in a neighboring PolyAnalysis directory that was not included in the reviewed package.

Mitigation: Install and use the skill only where that PolyAnalysis directory and virtual environment are controlled, reviewed, and trusted.

Risk: A Polygon RPC key may be used through a local .env file for on-chain data access.

Mitigation: Keep the RPC key least-privileged, rotate it if exposed, and avoid sharing logs or files that may reveal local secret values.

Risk: Wallet rankings and copy-trading reliability labels can be mistaken for financial advice or guaranteed future performance.

Mitigation: Present results as analytical signals, include the reliability rationale, and require user review before acting on trading decisions.

## Reference(s):

- [Leaderboard Discovery Strategies](references/leaderboard-strategies.md)
- [MM Score Details](references/mm-score-details.md)
- [Polymarket Leaderboard API](https://data-api.polymarket.com/v1/leaderboard)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and optional JSON output from the referenced analysis tool]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [User-facing output is expected to emphasize copy reliability labels, market-maker or HFT indicators, and copy trading score.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
