## Description: <br>
This skill connects to an MQTT broker and tracks messages from subscribed topics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[enchantedmotorcycle](https://clawhub.ai/user/enchantedmotorcycle) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to run a background MQTT client that connects with environment-provided broker settings and observes broker messages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The client may subscribe to and print all broker topics visible to the configured account. <br>
Mitigation: Use least-privilege MQTT credentials and prefer a version that honors MQTT_TOPIC or otherwise limits subscriptions to expected topics. <br>
Risk: MQTT payloads may be logged to stdout, which can expose sensitive message contents. <br>
Mitigation: Use only non-sensitive test topics or configure downstream logging to redact, restrict, or discard payload output. <br>
Risk: Connection details are loaded from a .env file before the client runs. <br>
Mitigation: Inspect the .env file before running bootstrap.sh and keep broker credentials scoped to the minimum required permissions. <br>


## Reference(s): <br>
- [MQTT Homepage](https://mqtt.org/) <br>
- [ClawHub Skill Page](https://clawhub.ai/enchantedmotorcycle/mqtt-client) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration] <br>
**Output Format:** [Plain text logs and shell command execution guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs for 60 seconds and prints received MQTT topics and payloads to stdout.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
