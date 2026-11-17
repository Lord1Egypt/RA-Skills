## Description:

Self-improving learning loop inspired by Hermes Agent that automatically extracts successful workflows, creates skills, and persists knowledge across sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mystour](https://clawhub.ai/user/mystour)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to periodically review completed work, extract reusable workflows into agent skills, and keep curated memory across OpenClaw sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates persistent agent memories and skills from session content with weak review and sanitization controls.

Mitigation: Keep automatic creation disabled, run the workflow manually, and review generated SKILL.md and memory files before reuse.

Risk: Session JSON or extracted workflow content may be untrusted or inappropriate for long-term agent memory.

Mitigation: Avoid untrusted session JSON and point memory and skills directories at isolated locations that can be inspected and deleted.

## Reference(s):

- [Hermes Agent](https://github.com/NousResearch/hermes-agent)
- [Hermes Docs](https://hermes-agent.nousresearch.com/)
- [agentskills.io specification](https://agentskills.io/specification)
- [SQLite FTS5 Docs](https://www.sqlite.org/fts5.html)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown files, generated SKILL.md content, CLI status text, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write persistent memory and skill files under configured OpenClaw directories.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
