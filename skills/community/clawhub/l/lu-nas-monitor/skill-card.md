## Description:

Lu Nas Monitor helps Chinese-language users check NAS Docker container status, system resource usage, service health, logs, and optional alerting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jesson1222-ship-it](https://clawhub.ai/user/jesson1222-ship-it)

### License/Terms of Use:

MIT

## Use Case:

Developers and NAS operators use this skill to ask an agent for concise Chinese-language monitoring guidance, Docker status checks, resource summaries, log inspection commands, service health checks, and alert setup examples for a NAS environment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Service restart guidance can interrupt running NAS services.

Mitigation: Review restart commands and target services before execution, and run them only during an acceptable maintenance window.

Risk: Telegram alerting can send NAS status or incident metadata to an external service.

Mitigation: Enable Telegram alerts only after confirming that tokens, chat targets, and external data sharing are acceptable for the environment.

Risk: Monitoring outputs may expose container names, ports, logs, and system capacity.

Mitigation: Limit sharing of generated monitoring output and redact operational details before sending results outside the environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jesson1222-ship-it/skills/lu-nas-monitor)
- [ClawHub publisher profile](https://clawhub.ai/user/jesson1222-ship-it)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Chinese-language Markdown responses with inline bash commands and monitoring snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Docker status summaries, system resource checks, log commands, restart commands, and optional Telegram alert setup.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
