## Description:

Captures, structures, and retrieves notes in local markdown, Apple Notes, Bear, Obsidian, Notion, or Evernote.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and developers use this skill to turn conversations, transcripts, quick captures, decisions, project updates, research notes, and note-corpus maintenance tasks into durable notes across local files and supported note apps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can keep durable local memory and update notes, action trackers, contacts, projects, indexes, and review files.

Mitigation: Install only if persistent note-management writes are expected, and review configured paths and write behavior before deployment.

Risk: Deletion and triage workflows may remove notes, actions, tags, or stale records.

Mitigation: Disable destructive sweeps or require explicit confirmation before deletion and bulk cleanup operations.

Risk: Credential and sensitive-note handling appears in the workflow and can expose secrets if copied into notes or temporary files.

Mitigation: Use pointer-based credential storage, avoid fixed /tmp note examples for sensitive content, and verify redaction before writing to synced or network-backed platforms.

Risk: Some supported platforms rely on third-party CLIs or network services.

Mitigation: Pin or independently review third-party CLIs before installation and confirm whether note content may leave the local machine for configured platforms.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/notes)
- [Skill homepage](https://clawic.com/skills/notes)
- [Publisher profile](https://clawhub.ai/user/ivangdavila)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands, note templates, configuration examples, and prose guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or update local note files, action trackers, indexes, review files, and app-specific note records according to user configuration.]

## Skill Version(s):

1.1.5 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
