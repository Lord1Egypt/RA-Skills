## Description: <br>
Deploy a fleet health monitoring system with 3 agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations engineers use this skill to configure three Pilot agents for fleet health monitoring, alert aggregation, and Slack or PagerDuty notification routing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Alert forwarding can send operational data to Slack or PagerDuty destinations. <br>
Mitigation: Confirm the destinations are approved for the organization and avoid forwarding secrets, customer data, or raw diagnostics in alert payloads. <br>
Risk: The setup establishes trust relationships between Pilot agents. <br>
Mitigation: Review the downstream Pilot bridge skills and approve only the intended agent handshakes before deployment. <br>
Risk: The setup writes a local Pilot manifest. <br>
Mitigation: Review the manifest contents before use and keep role, hostname, peer, and data-flow values aligned with the intended deployment. <br>


## Reference(s): <br>
- [Pilot Protocol](https://pilotprotocol.network) <br>
- [ClawHub Skill Page](https://clawhub.ai/teoslayer/pilot-fleet-health-monitor-setup) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with shell command examples and JSON manifest templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces role-specific setup instructions for Pilot monitor agents and an alert hub.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
