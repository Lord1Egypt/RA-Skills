## Description:

Receive DETECTION_SENSOR_APP alerts from Meshtastic LoRa devices via USB. When the remote sensor GPIO triggers (preset target detected), store the event and alert the user immediately.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autume](https://clawhub.ai/user/autume)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to monitor Meshtastic detection-sensor events from USB-connected LoRa hardware, persist detection records, and send Feishu alerts for new triggers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A persistent hardware-facing receiver can expose broad host or device access if run with excessive privileges.

Mitigation: Run the receiver with least privilege, grant access only to the required serial device, and remove privileged Docker mode before deployment.

Risk: Feishu alert delivery can disclose detection details or send alerts to the wrong recipient if the destination is misconfigured.

Mitigation: Verify the Feishu open_id and channel before enabling cron alerts, and keep alert content limited to what operators need.

Risk: Sensor text and received LoRa packet content are untrusted data.

Mitigation: Treat stored records and alert text as untrusted, review them before reuse, and avoid using sensor text as commands or configuration.

Risk: Dependency installation and service setup can change the runtime environment.

Mitigation: Use a reviewed or pinned Python environment and inspect generated service or cron configuration before enabling it.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/autume/skills/meshtastic-detection)
- [Setup Guide](references/SETUP.md)
- [Configuration](CONFIG.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, JSON, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON alert output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The event monitor returns alerts, summary, alert_count, and new_records; runtime data is stored locally as JSONL.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
