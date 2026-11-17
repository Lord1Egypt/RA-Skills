## Description:

Control and monitor the go-trader cryptocurrency trading system with natural language commands for strategies, status, risk, and emergency stops.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cyberleo986](https://clawhub.ai/user/cyberleo986)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect and control a local go-trader cryptocurrency trading service, including status checks, strategy mode changes, logs, and service stop/start actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: High-impact trading and service actions can stop, restart, reset, or switch the trading system into live operation.

Mitigation: Require explicit confirmation and authorization before live trading, stop, restart, emergency stop, or reset actions.

Risk: Raw trading logs and local service responses may expose sensitive operational or account information.

Mitigation: Restrict log access to authorized users and avoid exposing secrets or account identifiers in agent-visible output.

Risk: Emergency stop behavior may not match user expectations for open positions.

Mitigation: Document and verify whether emergency stop only stops the service or also manages open positions before using the skill with live funds.

## Reference(s):

- [Go Trader ClawHub Skill Page](https://clawhub.ai/cyberleo986/skills/go-trader)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and plain-text command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses can include raw service logs and JSON API responses from the local go-trader service.]

## Skill Version(s):

1.0.0 (source: server release metadata, created 2026-04-21)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
