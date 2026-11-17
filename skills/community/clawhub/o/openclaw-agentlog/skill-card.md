## Description:

openclaw-agentlog records OpenClaw agent session evidence and manages trace creation, claiming, completion, handoff, tool-call capture, response capture, reasoning capture, and Git commit binding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hobo0cn](https://clawhub.ai/user/hobo0cn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to automatically log agent sessions, tool activity, reasoning, responses, and trace handoffs to an AgentLog backend. It supports trace lifecycle management across agent task transfers and optional Git commit binding for session evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill captures sensitive agent data, including tool inputs, outputs, responses, and reasoning.

Mitigation: Install only where operators have explicitly accepted full trace logging, restrict access to the AgentLog backend, and disable reasoning or tool-call capture when those records should not be retained.

Risk: Automatic OpenClaw runtime patching can modify files outside the skill boundary during installation.

Mitigation: Avoid ordinary npm install until patching is removed or changed to an explicit admin-only step with clear rollback and OpenClaw version checks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hobo0cn/skills/openclaw-agentlog)
- [OpenClaw plugin schema](https://openclaw.ai/schemas/plugin.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with TypeScript API examples, shell commands, and JSON/YAML configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Captures trace and session records, tool inputs and outputs, reasoning summaries, responses, and optional Git commit bindings when enabled.]

## Skill Version(s):

1.1.2 (source: server release metadata; artifact package metadata reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
