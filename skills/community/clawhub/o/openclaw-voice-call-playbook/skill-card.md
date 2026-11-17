## Description:

Operate outbound voice calls safely with the OpenClaw voice-call plugin.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danielsinewe](https://clawhub.ai/user/danielsinewe)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to plan and execute clear, task-specific outbound calls through the OpenClaw voice-call plugin. It supports preflight checks, provider setup, dry runs, status checks, retries, and troubleshooting for operational reminders, alerts, verification, and escalation calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live outbound calls can incur provider costs or reach unintended recipients if credentials, caller numbers, destinations, or retry settings are wrong.

Mitigation: Confirm provider credentials, caller number, E.164 destination, and retry policy before each live call; test flows with the mock provider first.

Risk: Agent-initiated calls could contact real people without adequate user intent or an approved destination.

Mitigation: Require explicit user approval for each destination and call purpose, keep messages short and factual, and avoid open-ended chat flows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/danielsinewe/skills/openclaw-voice-call-playbook)
- [Publisher profile](https://clawhub.ai/user/danielsinewe)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces operational call playbooks, preflight checklists, provider configuration guidance, tool action guidance, and troubleshooting steps.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
