## Description: <br>
Universal MQTT Client for OpenClaw with Node.js/mqtt.js that enables connection management, subscription management, message handling, and OpenClaw integration for arbitrary MQTT-based automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sanwebgit](https://clawhub.ai/user/sanwebgit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation engineers use this skill to connect OpenClaw workflows to MQTT brokers, subscribe to topics, publish messages, monitor connection health, and trigger actions from MQTT state changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill writes persistent OpenClaw configuration when imported. <br>
Mitigation: Review ~/.openclaw/openclaw.json after installation and confirm the generated MQTT settings before use. <br>
Risk: Default broad MQTT subscriptions can expose more broker traffic than intended. <br>
Mitigation: Restrict subscriptions and publish permissions to specific topics instead of using # unless broad access is required. <br>
Risk: Credentialed TLS broker connections may not verify certificates safely. <br>
Mitigation: Avoid credentialed TLS connections until certificate verification is configured safely. <br>


## Reference(s): <br>
- [MQTT Topics Best Practices](references/mqtt-topics.md) <br>
- [mqtt.js Documentation](https://github.com/mqttjs/MQTT.js) <br>
- [MQTT 5.0 Specification](https://docs.oasis-open.org/mqtt/mqtt/v5.0/mqtt-v5.0.html) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with JavaScript examples, shell commands, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces MQTT integration guidance and reusable Node.js client code for OpenClaw workflows.] <br>

## Skill Version(s): <br>
1.2.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
