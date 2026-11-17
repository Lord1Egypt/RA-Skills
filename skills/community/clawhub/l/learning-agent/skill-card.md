## Description:

Captures learnings, errors, and corrections to enable continuous improvement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryan-wuxl](https://clawhub.ai/user/ryan-wuxl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to capture command failures, user corrections, knowledge gaps, feature requests, and reusable best practices as structured learning records. It also provides optional hook reminders and templates for promoting high-value learnings into agent or workspace guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Learning logs may capture sensitive prompts, secrets, tokens, command output, or transcript details.

Mitigation: Keep learning files project-scoped and redact sensitive content before writing entries.

Risk: Always-on hooks may inject persistent reminders or collect error context more broadly than intended.

Mitigation: Enable hooks only after review, prefer project-level hook configuration, and avoid global installation unless explicitly approved.

Risk: Promoting learnings into agent instruction or workspace memory files can change future agent behavior.

Mitigation: Require explicit human approval before adding entries to AGENTS.md, CLAUDE.md, SOUL.md, TOOLS.md, MEMORY.md, or similar persistent guidance.

Risk: Cross-session learning workflows may expose information from other sessions.

Mitigation: Review session-sharing actions before use and avoid sharing raw transcripts or private task context.

## Reference(s):

- [OpenClaw Integration](artifact/references/openclaw-integration.md)
- [Hook Setup Guide](artifact/references/hooks-setup.md)
- [Entry Examples](artifact/references/examples.md)
- [ClawHub Skill Page](https://clawhub.ai/ryan-wuxl/skills/learning-agent)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local learning logs, skill templates, hook configuration, and scaffolded skill files when explicitly used.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
