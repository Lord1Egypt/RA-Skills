## Description:

Noise Maker provides a planned alert gateway architecture for aggregating, filtering, correlating, and escalating webhook alerts from monitoring systems such as Zabbix and Graylog.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mbojer](https://clawhub.ai/user/mbojer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill as guidance for building an OpenClaw alert gateway that reduces noisy monitoring alerts, preserves alert history, and supports incident triage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release describes an alert gateway design whose implementation state is not complete.

Mitigation: Confirm which components are implemented before installing, building, or relying on the gateway operationally.

Risk: Webhook alert sources can be spoofed or abused if source validation is weakened.

Mitigation: Keep HMAC validation enabled for alert sources and use IP allowlists only as a secondary or transitional control.

Risk: Incident-closing and rule-toggling scripts could suppress or alter operational alerts.

Mitigation: Review those scripts and require deliberate operator approval before closing incidents or changing rule state.

Risk: LLM-driven suppression could hide important incidents if enabled too early or without review.

Mitigation: Run LLM behavior in passive mode first and require human approval before applying any suppression or defer rules.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mbojer/skills/noise-maker)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown planning guidance with SQL, Python, JSON, shell, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Planning document; server security evidence reports no bundled executable code or hidden behavior.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
