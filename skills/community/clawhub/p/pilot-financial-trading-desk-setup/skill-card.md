## Description:

Deploys a four-agent financial trading desk for coordinated market analysis, sentiment scanning, risk management, and trade execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to configure a coordinated trading workflow across analyst, sentiment, risk-management, and execution agents. It helps set up role-specific skills, hostnames, peer handshakes, and manifest data flows for a Pilot Protocol trading desk.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: High-impact trade execution workflows may place or route financial orders if connected to live exchange systems.

Mitigation: Use a sandbox or paper-trading environment until independent order limits or human approval gates are enforced.

Risk: Unpinned or unverified dependencies can change the behavior of the trading workflow.

Mitigation: Pin and verify all required skills and binaries, including pilotctl and clawhub, before installation.

Risk: Incorrect peer trust setup can route trade signals or approvals to unintended agents.

Mitigation: Manually verify each peer handshake and hostname before allowing data flows between agents.

Risk: Exchange credentials used by execution agents could allow excessive account access.

Mitigation: Use least-privilege exchange credentials and keep live trading permissions disabled until controls are reviewed.

## Reference(s):

- [Pilot Protocol](https://pilotprotocol.network)
- [ClawHub skill page](https://clawhub.ai/teoslayer/skills/pilot-financial-trading-desk-setup)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes role-specific install commands, hostname setup, handshake steps, manifest templates, and example Pilot Protocol messages.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
