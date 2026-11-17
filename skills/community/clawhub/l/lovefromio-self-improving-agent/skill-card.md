## Description:

Captures learnings, errors, and corrections so coding agents can record failures, user corrections, missing capabilities, outdated knowledge, and reusable improvements for later review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lovefromio](https://clawhub.ai/user/lovefromio)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to capture session learnings, command errors, corrections, and feature requests in markdown logs, then promote broadly applicable lessons into project or agent memory. It supports OpenClaw, Claude Code, Codex, GitHub Copilot, and generic agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to persist and promote session-derived content into future agent instructions.

Mitigation: Require human review before promoting content into CLAUDE.md, AGENTS.md, SOUL.md, TOOLS.md, or Copilot instructions.

Risk: Optional hooks can make self-improvement reminders broad or persistent across projects.

Mitigation: Keep hooks project-scoped when possible and avoid user-global hooks unless the operator explicitly wants global behavior.

Risk: Learning logs can accidentally capture sensitive context from conversations or command output.

Mitigation: Do not store secrets or raw transcripts in .learnings; summarize only the reusable lesson.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lovefromio/skills/lovefromio-self-improving-agent)
- [OpenClaw Integration](references/openclaw-integration.md)
- [Hook Setup Guide](references/hooks-setup.md)
- [Examples](references/examples.md)
- [Agent Skills Specification](https://agentskills.io/specification)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, configuration snippets, hook reminders, and generated skill scaffolds]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist learnings, errors, and feature requests to .learnings markdown files when the agent or operator follows the workflow.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
