## Description:

Guide creating Claude Code hooks with security-first design. Use for validation and enforcement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to plan, implement, and review Claude Code or Claude Agent SDK hooks for validation, logging, context injection, and workflow automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan flags reported fail-open validation and changes to global settings; its inspection was partial and does not establish whether flagged examples execute.

Mitigation: Review the relevant hook examples and settings changes before adopting them. Test error, timeout, and startup-failure behavior, and require explicit blocking behavior for guards where allowing the action would be unsafe.

## Reference(s):

- [Claude Code Hooks Documentation](https://docs.anthropic.com/en/docs/claude-code/hooks)
- [Claude Agent SDK Documentation](https://docs.anthropic.com/en/docs/claude-agent-sdk)
- [Claude Code Settings Configuration](https://docs.anthropic.com/en/docs/claude-code/settings)
- [Project homepage listed in skill metadata](https://github.com/athola/claude-night-market/tree/master/plugins/abstract)

## Skill Output:

**Output Type(s):** [Guidance, Code, Configuration instructions, Shell commands]

**Output Format:** [Markdown with JSON, Python, and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples and implementation guidance for authoring and testing hooks.]

## Skill Version(s):

1.10.4 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
