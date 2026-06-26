## Description: <br>
Forward Pilot Protocol events to HTTP webhooks for Slack, Discord, PagerDuty, and custom integrations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations engineers use this skill to forward Pilot Protocol events to external webhook-based services such as Slack, Discord, PagerDuty, Datadog, Microsoft Teams, and custom HTTP endpoints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Pilot event data may be sent to external webhook providers. <br>
Mitigation: Use HTTPS endpoints you control or trust, prefer selective source and topic subscriptions, and clear global webhook configuration when it is no longer needed. <br>
Risk: Forwarded events may contain secrets, personal data, or sensitive operational details. <br>
Mitigation: Redact sensitive values before forwarding and review event payloads before connecting production sources to third-party services. <br>


## Reference(s): <br>
- [Pilot Protocol](https://pilotprotocol.network) <br>
- [ClawHub Skill Page](https://clawhub.ai/teoslayer/pilot-webhook-bridge) <br>
- [Publisher Profile](https://clawhub.ai/user/teoslayer) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces webhook configuration and forwarding command examples; it does not generate persistent files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
