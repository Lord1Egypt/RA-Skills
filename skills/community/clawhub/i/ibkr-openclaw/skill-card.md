## Description:

Connect OpenClaw to Interactive Brokers via IB Gateway Docker for portfolio data, real-time quotes, historical K-lines, technical analysis, and Telegram alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[amuletxheart](https://clawhub.ai/user/amuletxheart)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users with Interactive Brokers accounts use this skill to configure IB Gateway Docker access and query portfolio, position, quote, and historical market data for monitoring and alerts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup relies on mutable installers, package installs, and a cloned Docker/Gateway dependency.

Mitigation: Review and pin Docker, Python package, and IB Gateway Docker versions before installation.

Risk: Brokerage credentials are stored in a plaintext .env file during setup.

Mitigation: Use a safer secret mechanism where possible, or restrict file permissions and host access before adding credentials.

Risk: Read-only configuration may not remove all operational or financial risk when connecting to a live brokerage account.

Mitigation: Prefer paper trading or least-privilege IBKR settings, verify read-only access before use, and monitor account permissions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/amuletxheart/skills/ibkr-openclaw)
- [IB Gateway Docker](https://github.com/gnzsnz/ib-gateway-docker)
- [ib_async](https://github.com/ib-api-reloaded/ib_async)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash, env, and Python snippets; CLI commands emit plain-text account, position, NAV, and quote summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an Interactive Brokers account, IB Gateway Docker, local API access, and Python dependencies.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
