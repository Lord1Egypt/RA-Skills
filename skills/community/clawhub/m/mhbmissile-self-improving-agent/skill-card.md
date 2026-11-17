## Description:

Captures learnings, errors, corrections, and feature requests so agents can improve future work and promote broadly useful guidance into project memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mhbmissile](https://clawhub.ai/user/mhbmissile)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to capture corrections, command errors, missing capabilities, knowledge gaps, and reusable practices as markdown learnings. The skill also guides review and human-approved promotion of durable lessons into agent memory files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent learning files can capture task details that influence future sessions.

Mitigation: Keep learning logs project-scoped and private by default, and redact secrets, credentials, personal data, and sensitive transcripts before saving.

Risk: Broad hooks can inject reminders or surface command-output-derived context across unrelated workspaces.

Mitigation: Prefer project-scoped hooks with restrictive matchers, and review hook configuration before enabling it globally.

Risk: Conversation-derived lessons can become incorrect or misleading if promoted directly into durable agent memory.

Mitigation: Require human review before promoting entries into AGENTS.md, CLAUDE.md, SOUL.md, TOOLS.md, or Copilot instructions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mhbmissile/skills/mhbmissile-self-improving-agent)
- [Hook Setup Guide](references/hooks-setup.md)
- [OpenClaw Integration](references/openclaw-integration.md)
- [Entry Examples](references/examples.md)
- [Agent Skills Specification](https://agentskills.io/specification)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce structured learning entries and suggest human-reviewed promotion into agent memory files.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
