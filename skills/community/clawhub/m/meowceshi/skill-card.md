## Description:

Captures learnings, errors, corrections, and feature requests in workspace markdown files so agents can reuse and promote recurring knowledge.

This skill is ready for commercial/non-commercial use.

## Publisher:

[j-meow-666](https://clawhub.ai/user/j-meow-666)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to capture command failures, user corrections, knowledge gaps, and feature requests into .learnings markdown logs. It also guides review and promotion of high-value learnings into project or agent instruction files after human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Session-derived guidance can persist into future agent instructions and influence later behavior.

Mitigation: Require human review before promoting entries into CLAUDE.md, AGENTS.md, SOUL.md, TOOLS.md, or Copilot instructions.

Risk: Hooks can automatically add reminders or inspect command output in broad contexts.

Mitigation: Keep hooks disabled by default or narrowly matched, and avoid global user-level hook configuration unless the workspace is trusted.

Risk: Learning logs may capture sensitive conversation details, secrets, transcripts, or command output.

Mitigation: Record short sanitized summaries, redact sensitive values, and avoid storing raw transcripts or full command output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/j-meow-666/skills/meowceshi)
- [OpenClaw Integration](references/openclaw-integration.md)
- [Hook Setup Guide](references/hooks-setup.md)
- [Entry Examples](references/examples.md)
- [Agent Skills specification](https://agentskills.io/specification)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can create or append .learnings markdown files and optionally suggest promotion into agent instruction files.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
