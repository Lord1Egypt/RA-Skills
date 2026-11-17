## Description:

Deploys a four-agent smart home coordinator that collects sensor data, resolves home automation goals, issues device commands, and displays home status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and smart-home operators use this skill to configure Pilot Protocol agents for sensor collection, decision routing, device actuation, and dashboard reporting across a home automation deployment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup can connect agents that control real smart-home devices.

Mitigation: Review the deployment before installation, verify peer identities before handshakes, and test commands in a non-critical environment before controlling physical devices.

Risk: Trust is auto-approved after reciprocal handshakes.

Mitigation: Use a simple unique hostname prefix, confirm each peer hostname out of band, and inspect trust state with pilotctl before publishing device commands.

Risk: Dashboard summaries can send home-state data to external services such as Slack, webhooks, or email.

Mitigation: Enable external summaries only after confirming what home-state data leaves the local network and limiting recipients to trusted destinations.

Risk: The setup installs dependent skills and relies on local Pilot Protocol tooling.

Mitigation: Use pinned and trusted dependency versions for Pilot Protocol skills, pilotctl, and clawhub, and confirm the daemon is running before use.

## Reference(s):

- [Pilot Protocol homepage](https://pilotprotocol.network)
- [ClawHub skill page](https://clawhub.ai/teoslayer/skills/pilot-smart-home-coordinator-setup)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and JSON manifest templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces role-specific setup instructions for four Pilot Protocol agents.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
