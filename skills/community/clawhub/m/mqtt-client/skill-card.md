## Description:

This is a simple client for connecting to an mqtt instance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[enchantedmotorcycle](https://clawhub.ai/user/enchantedmotorcycle)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to run a background MQTT client that connects to a broker, subscribes to messages, and logs received topic payloads.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The client subscribes broadly to broker topics, which can expose more message data than intended.

Mitigation: Use a dedicated least-privileged MQTT account and narrow the subscription topic before deployment.

Risk: Raw MQTT payload logging can disclose sensitive message contents.

Mitigation: Disable payload logging or redact message contents before using the skill with sensitive brokers.

Risk: Shell-sourcing a .env file can mishandle credentials or execute unintended shell content.

Mitigation: Replace shell-sourcing with safe parsing of named configuration keys and restrict access to the configuration file.

Risk: Non-local MQTT connections without TLS can expose broker traffic and credentials.

Mitigation: Require TLS for non-local broker connections.

## Reference(s):

- [MQTT project website](https://mqtt.org/)
- [ClawHub skill page](https://clawhub.ai/enchantedmotorcycle/skills/mqtt-client)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration]

**Output Format:** [Plain text logs and shell command execution]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python and MQTT connection details from environment variables.]

## Skill Version(s):

1.0.7 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
