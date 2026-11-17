## Description:

Captures agent learnings, command errors, user corrections, feature requests, and recurring best practices so future coding sessions can update local learning logs and project memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ingjosemendez](https://clawhub.ai/user/ingjosemendez)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding-agent users use this skill to record corrections, failures, knowledge gaps, and reusable practices, then promote high-value lessons into agent memory or project guidance files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent learning logs can capture conversation-derived secrets, personal data, raw transcripts, or credentials.

Mitigation: Redact sensitive content before writing learning entries and keep logs scoped to the project or workspace where they are needed.

Risk: Promoting lessons into future agent guidance files can change later agent behavior in incorrect or misleading ways.

Mitigation: Require confirmation before writes and review diffs to CLAUDE.md, AGENTS.md, SOUL.md, TOOLS.md, and copilot instructions before accepting promoted guidance.

Risk: Globally enabled hooks can inject reminders across unrelated projects.

Mitigation: Prefer project-scoped hook activation and avoid global activation unless the user has explicitly chosen that behavior.

## Reference(s):

- [OpenClaw Integration](references/openclaw-integration.md)
- [Hook Setup Guide](references/hooks-setup.md)
- [Entry Examples](references/examples.md)
- [Agent Skills Specification](https://agentskills.io/specification)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command snippets, hook configuration examples, and learning-entry templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide creation or updates of .learnings files and agent guidance files when the user approves those changes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
