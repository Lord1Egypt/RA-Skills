## Description:

Trade Polymarket markets based on valuation divergence. When your probability model differs from Polymarket's price by >threshold, enter using Kelly sizing. Works with any probability model (Simmer AI consensus, user model, external API).

This skill is ready for commercial/non-commercial use.

## Publisher:

[adlai88](https://clawhub.ai/user/adlai88)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to scan Polymarket markets for divergence between a probability model and market prices, size potential positions with Kelly-style limits, and optionally execute trades through Simmer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Simmer API key that may read account data and can place trades when live mode is used.

Mitigation: Start in dry-run mode and use a dedicated low-limit or read-only key where possible.

Risk: Live mode can execute real Polymarket trades.

Mitigation: Use live mode only after reviewing the configuration, edge threshold, position cap, trade limit, and model behavior.

Risk: The required simmer-sdk dependency is not pinned in the release metadata.

Mitigation: Pin and review the simmer-sdk version before deployment.

Risk: Non-Simmer probability models are described as customization options but require code edits before use.

Mitigation: Review and test any custom probability model changes before enabling live trading.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/adlai88/skills/polymarket-valuation-divergence)
- [Publisher profile](https://clawhub.ai/user/adlai88)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and terminal status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce dry-run trading signals, live execution status, configuration summaries, and portfolio status output.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
