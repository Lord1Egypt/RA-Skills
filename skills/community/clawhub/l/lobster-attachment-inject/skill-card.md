## Description:

Provides guidance for injecting dynamic skill, agent, and memory context as attachment-style content instead of modifying the system prompt.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangxiaofei860208-source](https://clawhub.ai/user/wangxiaofei860208-source)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent maintainers use this skill to reduce repeated prompt content by keeping lightweight registries and loading full skill or agent definitions only when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent to read additional agent and skill definitions, which may introduce unwanted context if loaded without confirmation.

Mitigation: Use explicit routing or confirmation before loading additional agents or skills.

Risk: Registry or AGENTS.md injection content may be updated outside the intended files.

Mitigation: Scope write access to the intended registry and configuration files before use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wangxiaofei860208-source/skills/lobster-attachment-inject)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell command examples and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable files are bundled in the artifact.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
