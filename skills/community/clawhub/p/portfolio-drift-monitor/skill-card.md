## Description:

Real-time Kalshi portfolio drift alerts that monitor positions and fire when any position moves beyond the configured threshold since the last check.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kingmadellc](https://clawhub.ai/user/kingmadellc)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to monitor Kalshi portfolio positions, compare the current state with a local snapshot, and receive alerts when position, P&L, or price drift exceeds a configured threshold.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires Kalshi API access and reads a private key file path configured by the user.

Mitigation: Install only when Kalshi API access is appropriate, protect the key file, restrict file permissions, and avoid exposing credential values in logs or shared debug output.

Risk: Portfolio state and drift alerts may reveal sensitive trading positions, and configured Slack delivery can transmit those details outside the local machine.

Mitigation: Review or remove Slack webhook configuration before use and treat alert messages and ~/.openclaw/state/portfolio_snapshot.json as sensitive portfolio data.

Risk: The artifact includes behavior guidance for agents to persistently modify installed source files.

Mitigation: Review proposed code changes before applying them and scan updated skill files before redeployment.

## Reference(s):

- [Portfolio Drift Monitor Configuration Reference](references/drift-config.md)
- [Kalshi API Documentation](https://docs.kalshi.com)
- [Portfolio Drift Monitor on ClawHub](https://clawhub.ai/kingmadellc/skills/portfolio-drift-monitor)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown-style text with shell command examples and console alert output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write a local portfolio snapshot under ~/.openclaw/state and may send configured Slack notifications.]

## Skill Version(s):

1.1.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
