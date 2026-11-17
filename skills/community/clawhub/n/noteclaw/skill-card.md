## Description:

Mirrors OneNote notebooks read-only into local Markdown and git history so an agent can search notes, compare changes, and write periodic summaries after one-time Microsoft account authorization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jellyjujube](https://clawhub.ai/user/jellyjujube)

### License/Terms of Use:

MIT-0 (MIT No Attribution)

## Use Case:

People and agents with personal Microsoft accounts use this skill to keep a local, searchable history of OneNote notes and generate change reports without editing OneNote.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: OneNote section or section-group names may cause writes or deletes outside the intended mirror folder.

Mitigation: Until the path-handling flaw is fixed, avoid syncing notebooks with section names controlled by others and use a dedicated private data directory without unrelated files.

Risk: Microsoft authorization grants account read access, and the bundled public application may receive broader OneDrive read access than the notes need.

Mitigation: Review permissions before authorizing; use a separately registered application requesting only Notes.Read if narrower access is needed, and protect the locally stored refresh token.

Risk: Mirrored note content persists in local git history and may expose sensitive information if shared.

Mitigation: Keep the mirror and git history private, and ensure authentication files are excluded from commits.

## Reference(s):

- [noteClaw on ClawHub](https://clawhub.ai/jellyjujube/skills/noteclaw)
- [Weekly report workflow](references/weekly-report.md)
- [rclone OneDrive authorization documentation](https://rclone.org/onedrive/)

## Skill Output:

**Output Type(s):** [Markdown, Text, Shell commands, Configuration instructions]

**Output Format:** [Local Markdown files, text query results, and git snapshots]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports summarize changes in mirrored notes; images are represented by placeholders.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata and CHANGELOG.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
