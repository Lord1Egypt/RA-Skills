## Description:

Manage Pi Agent as a sub-agent for complex coding tasks involving multiple files, extensive refactoring, or systemic debugging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hybrid1labs](https://clawhub.ai/user/hybrid1labs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to route complex OpenClaw coding work to Pi Agent when a task spans many files, requires substantial refactoring, or needs systemic debugging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs users or agents to install and run a third-party coding agent globally, including background execution.

Mitigation: Use only if the Pi npm package is trusted; prefer a pinned, project-local or sandboxed installation.

Risk: Delegated coding tasks can change project files with weak scoping.

Mitigation: Require explicit user approval before long-running background tasks or changes to OpenClaw agent configuration, and review resulting changes before integration.

Risk: Passing untrusted task text through shell command strings can create command-handling risk.

Mitigation: Avoid passing untrusted task text through shell strings; quote and review prompts before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hybrid1labs/skills/pi-coding-specialist)
- [ClawHub publisher profile](https://clawhub.ai/user/hybrid1labs)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May delegate long-running coding tasks to a third-party Pi CLI process that can modify project files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
