## Description: <br>
Deploy a feedback collection pipeline with 3 agents that automate intake, sentiment analysis, and actionable routing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and customer experience teams use this skill to configure a three-agent Pilot Protocol workflow that collects feedback, analyzes sentiment, and routes actionable issues to product, engineering, or support channels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Customer feedback may include identifiers, ticket URLs, or raw text that should not be routed to shared or external channels. <br>
Mitigation: Redact customer identifiers, ticket URLs, and sensitive feedback text before forwarding feedback to Slack, webhooks, or other shared destinations. <br>
Risk: The setup depends on local pilotctl and clawhub binaries plus configured handshake and webhook targets. <br>
Mitigation: Use trusted binaries and verify peer hostnames, handshake targets, Slack channels, and webhook destinations before running the setup commands. <br>


## Reference(s): <br>
- [Pilot Protocol](https://pilotprotocol.network) <br>
- [ClawHub Skill Page](https://clawhub.ai/teoslayer/pilot-feedback-collector-setup) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes role-specific setup manifests, hostnames, handshakes, and example publish/subscribe commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
