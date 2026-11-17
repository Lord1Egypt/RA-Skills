## Description:

OpenClaw Usage Dashboard provides a localhost dashboard for OpenClaw usage, model activity, token consumption, agent activity, and system health from local session logs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vanhuelsing](https://clawhub.ai/user/vanhuelsing)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to launch a local dashboard that summarizes token usage, request counts, model and agent activity, cache efficiency, and system health from OpenClaw session logs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private OpenClaw usage patterns, model choices, agent names, session timing, and system details can be exposed through unauthenticated dashboard APIs.

Mitigation: Run only with the default localhost binding and do not use --host 0.0.0.0 or any other non-loopback address.

Risk: Server evidence reports a verified browser security flaw and marks the release suspicious.

Mitigation: Review the skill before installing, especially on shared or networked machines, and use it only in a trusted local browser environment.

## Reference(s):

- [OpenClaw Usage Dashboard on ClawHub](https://clawhub.ai/vanhuelsing/skills/openclaw-usage-dashboard)
- [OpenClaw Rate Limits Tracking Issue](https://github.com/openclaw/openclaw/issues/55934)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide the user to run a local Node.js dashboard on a selected localhost port.]

## Skill Version(s):

2.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
