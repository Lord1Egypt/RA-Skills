## Description:

Monitor LibreNMS network devices, health sensors, port statistics, and unresolved active alerts through read-only API calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[florianbeer](https://clawhub.ai/user/florianbeer)

### License/Terms of Use:


## Use Case:

Developers, infrastructure operators, and network administrators use this skill to ask an agent for LibreNMS status summaries, down-device triage, health checks, port statistics, and active alert reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends the LibreNMS API token while TLS certificate verification is disabled by default.

Mitigation: Remove curl's -k/-sk default, use a trusted CA or --cacert for self-signed LibreNMS certificates, and keep the token limited to minimum read-only server-side permissions.

Risk: The API token or generated monitoring reports could be exposed if stored with broad permissions or written to shared temporary paths.

Mitigation: Keep the config file private, restrict permissions on the credentials file, and avoid saving reports to shared /tmp paths.

## Reference(s):

- [LibreNMS API Documentation](https://docs.librenms.org/API/)
- [ClawHub LibreNMS Skill Page](https://clawhub.ai/florianbeer/skills/librenms)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal-oriented text with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only LibreNMS API responses are summarized for device status, alerts, health sensors, and port statistics.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
