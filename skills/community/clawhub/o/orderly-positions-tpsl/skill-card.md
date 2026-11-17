## Description:

Monitor positions in real-time, configure Take-Profit/Stop-Loss orders, and manage risk with leverage settings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tarnadas](https://clawhub.ai/user/tarnadas)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to build Orderly position management interfaces, monitor PnL and margin data, configure TP/SL orders, and adjust leverage for perpetual futures workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live trading operations can close positions, change leverage, place TP/SL orders, stop orders, or cancel orders without clear safety guardrails.

Mitigation: Use sandbox or paper trading first and require explicit user confirmation before executing trading actions.

Risk: Orderly credentials with broad trading permissions can expose real accounts to unintended market actions.

Mitigation: Restrict API permissions where possible and review the skill carefully before using it with real Orderly credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tarnadas/skills/orderly-positions-tpsl)

## Skill Output:

**Output Type(s):** [Guidance, Code, API Calls, Configuration instructions]

**Output Format:** [Markdown with TypeScript examples and REST API request shapes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes position, leverage, TP/SL, stop order, cancellation, PnL, margin, and liquidation-risk guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
