## Description:

Deploy a log analytics system with 4 agents for collection, parsing, alerting, and visualization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill to configure a four-agent Pilot Protocol log analytics deployment for centralized log collection, parsing, anomaly alerting, and dashboard reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup installs multiple dependent skills and creates persistent Pilot trust and configuration state.

Mitigation: Review dependent skills before installation, restrict deployments to approved peers, verify peer identities before handshakes, and back up any existing ~/.pilot setup file.

Risk: Log reports may contain sensitive raw logs or secrets and can be forwarded to Slack or webhooks.

Mitigation: Limit approved log sources and outbound destinations, redact secrets before forwarding, and avoid sending raw logs to external channels.

## Reference(s):

- [Pilot Protocol](https://pilotprotocol.network)
- [ClawHub skill page](https://clawhub.ai/teoslayer/skills/pilot-log-analytics-setup)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides role selection, dependent skill installation, Pilot hostname setup, manifest creation, peer handshakes, and example log event publishing.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
