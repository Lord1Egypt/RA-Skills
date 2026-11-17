## Description:

Gmail, Contacts, Calendar, Drive (with comments), Docs, and Sheets for OpenClaw agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[panthrocorp](https://clawhub.ai/user/panthrocorp)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw agents and operators use this skill to read Gmail, contacts, calendar events, Drive files, Docs, and Sheets, with opt-in write modes for calendar events, Drive comments, Docs edits, and Sheets writes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release guidance includes installing a binary that may be mutable or unverified.

Mitigation: Use a pinned release and verify the SHA-256 checksum or signature before installing the binary.

Risk: OAuth setup guidance can lead users to weaken Google Advanced Protection.

Mitigation: Do not disable Advanced Protection for a primary account; use an administrator-approved OAuth client or a dedicated least-privilege Google account.

Risk: Readwrite modes and command output can expose or modify private Google Workspace data.

Mitigation: Keep readwrite modes disabled unless explicitly needed, and treat command output as sensitive workspace data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/panthrocorp/skills/panthrocorp-google-workspace)
- [Project homepage](https://github.com/PanthroCorp-Limited/openclaw-skills)
- [Google Cloud Console](https://console.cloud.google.com/)

## Skill Output:

**Output Type(s):** [JSON, Text, Shell commands, Configuration]

**Output Format:** [JSON by default; plain text where supported]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Google OAuth credentials, an encrypted token key, the google-workspace binary, and service modes that control readonly or readwrite behavior.]

## Skill Version(s):

0.5.2 (source: SKILL.md frontmatter, evidence release metadata, artifact/dist/metadata.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
