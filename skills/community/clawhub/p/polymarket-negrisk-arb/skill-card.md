## Description:

Scans multi-outcome Polymarket markets for mathematical arbitrage and can execute simultaneous batch trades when aggregate outcome pricing falls below configured thresholds.

This skill is ready for commercial/non-commercial use.

## Publisher:

[r2crypto](https://clawhub.ai/user/r2crypto)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and trading operators use this skill to scan multi-outcome prediction markets for price-sum arbitrage opportunities and optionally place all required outcome trades as a batch.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automated financial trading can create real-money loss even when an opportunity appears mathematically favorable.

Mitigation: Start in dry-run or paper-trading mode, keep paper trading enabled until review is complete, and use live trading only after accepting loss risk.

Risk: The security evidence reports unattended live quiet execution and says the claimed safeguards are not reliably enforced.

Mitigation: Do not enable the managed live automaton until trade safeguards, budget limits, dependency provenance, and API-key scope have been independently verified.

Risk: The skill requires a SIMMER_API_KEY for market and trading API access.

Mitigation: Use a restricted API key when available and rotate it if the execution environment is shared or compromised.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/r2crypto/skills/polymarket-negrisk-arb)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with shell commands, Python code, JSON output, and configuration settings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SIMMER_API_KEY; dry-run scanning is available, while live trading is enabled with explicit runtime or automaton settings.]

## Skill Version(s):

1.0.2 (source: server release evidence, artifact metadata, clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
