## Description:

Simple text-based memory system for AI assistants - auto-install script included

This skill is ready for commercial/non-commercial use.

## Publisher:

[crystaria](https://clawhub.ai/user/crystaria)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI assistant users use Memory Boost to create and maintain local Markdown memory files for preferences, project history, decisions, quick indexes, and daily session logs across conversations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory files can accumulate sensitive preferences, project context, or personal data across sessions.

Mitigation: Restrict memory files to a specific project location, avoid storing secrets or sensitive personal data, and periodically review or delete retained notes.

Risk: Automatically loaded memory can contain outdated, incorrect, or adversarial notes that influence future assistant behavior.

Mitigation: Treat memory content as untrusted context, review it before relying on it, and confirm important decisions with the user before acting.

Risk: Automatic writes may record information the user did not intend to preserve.

Mitigation: Review every proposed memory write and require explicit approval before adding durable preferences, decisions, or project history.

## Reference(s):

- [ClawHub skill homepage](https://clawhub.ai/skills/memory-boost)
- [ClawHub skill page](https://clawhub.ai/crystaria/skills/memory-boost)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and local file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local Markdown memory files such as MEMORY.md, MEMORY_INDEX.md, and daily logs when the install script is run.]

## Skill Version(s):

1.1.1 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
