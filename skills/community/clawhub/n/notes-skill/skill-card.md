## Description:

A SQLite-based OpenClaw notes management skill that helps an agent create, search, list, archive, and back up local notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cocoonovo](https://clawhub.ai/user/cocoonovo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and OpenClaw operators use this skill to manage personal or workspace notes through an AI assistant, including capture, retrieval, organization, archiving, and backup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores notes persistently in a local SQLite database and backups, which can retain sensitive information.

Mitigation: Avoid storing secrets or regulated data, review local file permissions, and confirm backup retention before use.

Risk: Broad note-related triggers can cause the agent to act on ambiguous requests.

Mitigation: Use explicit note commands and confirm intent before creating, archiving, or backing up notes.

Risk: The artifact references initialization and backup scripts that were not included for review.

Mitigation: Install only after reviewing the actual scripts and prefer implementations with parameterized database operations and clear deletion or purge controls.

## Reference(s):

- [Skill instructions](artifact/SKILL.md)
- [README](artifact/README.md)
- [ClawHub skill page](https://clawhub.ai/cocoonovo/skills/notes-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with SQL and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces notes-management guidance and command examples for local SQLite storage and backups.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
