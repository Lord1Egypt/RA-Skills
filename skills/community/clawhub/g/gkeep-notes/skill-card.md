## Description:

Google Keep notes via gkeepapi. List, search, create, manage notes. Add items to notes. Supports authorization via OAuth 2.0 Token.

This skill is ready for commercial/non-commercial use.

## Publisher:

[promptingpufferfish](https://clawhub.ai/user/promptingpufferfish)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent manage Google Keep notes through a local Python CLI, including listing, searching, creating, reading, updating, archiving, deleting, pinning, and checking note items.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill needs read/write access to Google Keep notes.

Mitigation: Install only for accounts where agent access to note content and note modification is acceptable; review note IDs before archive, delete, pin, unpin, check, or add actions.

Risk: Token setup requires manually handling reusable Google authentication material.

Mitigation: Do not paste browser cookies or tokens into chats, logs, or shared terminals; restrict token.json permissions and prefer an official OAuth flow if available.

Risk: The skill depends on an unofficial Google Keep API that may break if Google changes behavior.

Mitigation: Treat API failures as a maintenance signal and review upstream compatibility before relying on the skill for critical workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/promptingpufferfish/skills/gkeep-notes)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and command output text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and local Google Keep authentication material stored in token.json.]

## Skill Version(s):

1.0.14 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
