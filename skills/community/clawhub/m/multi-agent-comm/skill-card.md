## Description:

Multi-Agent Communication Protocol is a general OpenClaw framework for structured communication, task delegation, parallel subagent orchestration, and shared context across agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ncepuee](https://clawhub.ai/user/ncepuee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to coordinate OpenClaw agents, delegate tasks to subagents, maintain persistent sessions, configure ACP-based agent communication, and summarize parallel work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags this skill as suspicious because it encourages persistent agents, session resumption, and environment/API-key sharing without enough safety guidance.

Mitigation: Review before installation when agents can access email, documents, calendars, API keys, or prior session history; use only trusted subagents and avoid broad environment inheritance.

Risk: Resumed sessions and cross-agent communication can route work to the wrong identity, context, or task if session ownership is not checked.

Mitigation: Verify that any resumed session belongs to the intended user and task before sending new instructions or shared context.

Risk: Copying secrets or sharing inherited environments across devices and agents can increase credential exposure.

Mitigation: Rotate or provision per-device API keys rather than copying secrets casually.

## Reference(s):

- [ACP Setup Guide](references/acp-setup.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline session, ACP, YAML, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces operational guidance for spawning, steering, resuming, and configuring multi-agent sessions.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
