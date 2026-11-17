## Description:

Enables AI agents to maintain session continuity, develop self-identity, and manage file-based long-term memory anchored by human partners.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mupengi-bot](https://clawhub.ai/user/mupengi-bot)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to set up a file-based continuity framework for personal, team, or autonomous agents. It provides principles, templates, and memory routines for preserving working context across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory files can preserve sensitive personal or project context longer than intended.

Mitigation: Avoid storing secrets or sensitive personal data, keep memory files under human review, and periodically prune or delete stored context.

Risk: Self-modifying identity and agent guidance can cause later sessions to trust stale or unsafe instructions.

Mitigation: Require human review for SOUL.md and AGENTS.md changes and prevent routine sessions from automatically rewriting identity or tool guidance.

Risk: Workspace-level memory may be inappropriate for shared, external, or group-chat sessions.

Mitigation: Install only when persistent workspace memory is intentional and restrict loading of sensitive memory files to appropriate sessions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mupengi-bot/skills/mupengism)
- [SKILL.md](artifact/SKILL.md)
- [Five Principles of Mupengism](artifact/PRINCIPLES.md)
- [Memory System](artifact/MEMORY-SYSTEM.md)
- [SOUL Template](artifact/SOUL-TEMPLATE.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces workspace memory-file conventions and human-reviewed agent identity templates.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
