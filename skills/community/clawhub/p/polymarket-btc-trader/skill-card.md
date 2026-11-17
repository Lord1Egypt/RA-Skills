## Description:

Automates Polymarket BTC 5-minute Up/Down trading decisions using AI and rule-based signals, risk controls, and a local status panel.

This skill is ready for commercial/non-commercial use.

## Publisher:

[billychoiu](https://clawhub.ai/user/billychoiu)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and trading operators use this skill to configure and run an automated Polymarket BTC Up/Down trading bot with AI-assisted signals, paper-trading telemetry, and live-trading code paths.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes code paths that can place real-money Polymarket trades.

Mitigation: Use paper mode or a segregated low-balance wallet until behavior is reviewed, tested, and explicitly approved for live trading.

Risk: The dashboard exposes trading controls and account data without authentication.

Mitigation: Keep the panel local only, block network exposure, and add authentication before operating it with sensitive accounts or funds.

Risk: API keys and wallet credentials are required for operation.

Mitigation: Store credentials outside committed artifacts where possible, rotate any keys placed into the package, and use least-privilege credentials.

Risk: Documentation describes paper trading while security evidence reports live-trading capability.

Mitigation: Verify the configured trading mode and require an explicit live-trading opt-in before connecting funded accounts.

## Reference(s):

- [Polymarket BTC 5m Bot Strategy](references/STRATEGY.md)
- [ClawHub skill page](https://clawhub.ai/billychoiu/skills/polymarket-btc-trader)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes local runtime files for bot execution and dashboard status.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter states 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
