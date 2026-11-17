## Description:

Scans Polymarket markets for YES/NO price gaps and can optionally execute paired Fill-or-Kill trades using a configured wallet.

This skill is ready for commercial/non-commercial use.

## Publisher:

[themsquared](https://clawhub.ai/user/themsquared)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and trading tool operators use this skill to scan Polymarket markets for potential YES/NO arbitrage and review or execute paired orders with configured risk controls. Live execution should be treated as financially sensitive because the server security summary warns that the order handling may leave unexpected exposure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary states that sequential order execution can leave a user with unexpected financial exposure despite no-position claims.

Mitigation: Run scan-only by default, use a dedicated low-balance wallet, and avoid live --buy execution until order handling detects, reports, and manages partial execution.

Risk: Live trading requires private-key and wallet access.

Mitigation: Pin and review dependencies before running with private-key access, and keep credentials limited to a dedicated wallet with minimal funds.

Risk: The artifact presents arbitrage as risk-free, while the authoritative security guidance says not to rely on those guarantees.

Mitigation: Treat opportunities as proposals, manually verify price, liquidity, fees, and execution assumptions, and use conservative --min-edge and --max-deploy settings.

## Reference(s):

- [Polymarket Arb Scanner Pro on ClawHub](https://clawhub.ai/themsquared/skills/polymarket-arb-scanner-pro)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and command-line text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May report market-scan results, arbitrage candidates, balance checks, and order execution status when live trading is enabled.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
