## Description:

Monitor system health on the gateway host (Raspberry Pi, ARM, or Linux), reporting CPU, RAM, disk, temperature, uptime, load, top processes, and threshold alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lookupmark](https://clawhub.ai/user/lookupmark)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect local gateway host health on Raspberry Pi, ARM, or Linux systems and check threshold alerts before service issues escalate.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reports can expose local process metadata, including usernames and process command lines.

Mitigation: Install only where users may view that metadata, avoid broad sharing unless command lines are removed or opt-in, and avoid elevated privileges unless necessary.

## Reference(s):

- [ClawHub System Monitor Skill Page](https://clawhub.ai/lookupmark/skills/lookupmark-system-monitor)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Plain text or JSON status reports with optional alert lines and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports local system metrics and may include usernames and sanitized process command lines.]

## Skill Version(s):

1.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
