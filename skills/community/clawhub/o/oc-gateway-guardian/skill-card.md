## Description:

Protect long-running OpenClaw gateways from unsafe restarts with preflight checks, watchdog diagnosis, and evidence capture.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiepu110](https://clawhub.ai/user/jiepu110)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to diagnose OpenClaw gateway instability, decide whether a restart is safe, and capture evidence before taking disruptive action.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent to run diagnostics and, with user direction, restart an OpenClaw gateway.

Mitigation: Confirm the referenced OpenClaw guardian scripts are the expected workspace scripts before installing or using the skill, and require explicit user acceptance before forced restarts.

Risk: A gateway restart can interrupt active OpenClaw tasks or embedded runs.

Mitigation: Run the documented preflight check before restart, honor BLOCK results, and prefer diagnosis or cooldown when active work or recent stability heartbeats are present.

Risk: Generated diagnostic reports may include local gateway status, task, or log evidence.

Mitigation: Treat diagnostic reports as sensitive operational material and review them before sharing outside the local workspace.

## Reference(s):

- [OpenClaw Gateway Guardian Failure Modes](references/failure_modes.md)
- [ClawHub Skill Page](https://clawhub.ai/jiepu110/skills/oc-gateway-guardian)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Markdown, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and diagnostic interpretation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct agents to produce diagnostic reports under the configured OpenClaw diagnostics directory.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
