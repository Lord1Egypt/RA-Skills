## Description:

Universal MQTT Client for OpenClaw with Node.js/mqtt.js. Enables Connection Management, Subscription Management, Message Handling and OpenClaw Integration for arbitrary MQTT-based automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sanwebgit](https://clawhub.ai/user/sanwebgit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation engineers use this skill to connect OpenClaw agents to MQTT brokers, subscribe to topics, publish messages, monitor health, and trigger actions from MQTT state changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can handle MQTT credentials and persistent OpenClaw configuration in ways that may weaken or redirect secure connections.

Mitigation: Review before installing, use least-privilege MQTT accounts, secure ~/.openclaw/openclaw.json permissions, pin dependencies, and fix TLS certificate verification before using real credentials.

Risk: Broad MQTT subscriptions such as the # wildcard can expose more broker traffic than intended.

Mitigation: Avoid # except on trusted scoped brokers and prefer narrowly scoped topic filters for production automation.

Risk: Running the skill from untrusted project directories can expose local configuration behavior to untrusted files or workflows.

Mitigation: Run it only from trusted workspaces and review configuration changes before deployment.

## Reference(s):

- [MQTT Topics Best Practices](references/mqtt-topics.md)
- [mqtt.js Documentation](https://github.com/mqttjs/MQTT.js)
- [MQTT 5.0 Specification](https://docs.oasis-open.org/mqtt/mqtt/v5.0/mqtt-v5.0.html)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JavaScript, JSON, and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include MQTT topic patterns, environment variables, OpenClaw configuration, and usage examples.]

## Skill Version(s):

1.2.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
