## Description:

Provides example OpenClaw hooks for intercepting, modifying, blocking, logging, model switching, and subagent event handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hanxiao-bot](https://clawhub.ai/user/hanxiao-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill as example guidance for OpenClaw plugin hooks that audit tool calls, block selected actions, validate parameters, switch models, and route subagent results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Example snippets log tool parameters and session identifiers.

Mitigation: Redact sensitive tool parameters and session identifiers before adapting any logging example.

Risk: Substring command checks can miss dangerous variants or block benign commands.

Mitigation: Replace illustrative substring checks with scoped allowlists, sandboxing, and explicit approval for dangerous operations.

Risk: Hook examples that block tools or switch models can change agent behavior if copied into a plugin.

Mitigation: Review and test adapted hooks in a controlled environment before deployment.

## Reference(s):

- [OpenClaw Hook Examples on ClawHub](https://clawhub.ai/hanxiao-bot/skills/openclaw-hook-examples)
- [hanxiao-bot publisher profile](https://clawhub.ai/user/hanxiao-bot)
- [Artifact skill source](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Configuration]

**Output Format:** [Markdown with JavaScript code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only examples; snippets require review and adaptation before use.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
