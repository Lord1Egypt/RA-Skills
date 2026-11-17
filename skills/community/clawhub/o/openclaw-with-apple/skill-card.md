## Description:

Apple iCloud full-service access, Apple Health analysis, and bidirectional task and notes sync for AI agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gzww](https://clawhub.ai/user/gzww)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to connect an AI assistant with Apple iCloud services, analyze exported Apple Health data, and sync conversational tasks or notes into iPhone Reminders and Notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to provide Apple ID primary passwords and 2FA codes to an AI chat.

Mitigation: Prefer Apple app-specific passwords for calendar-only use and use local interactive authentication rather than pasting primary credentials or 2FA codes into chat.

Risk: Cached iCloud sessions under ~/.pyicloud may allow account access while the session remains valid.

Mitigation: Limit filesystem access, verify ~/.pyicloud permissions, and remove cached sessions when the skill is no longer needed.

Risk: Automatic background syncing can upload local tasks, notes, or health-derived files to iCloud Drive without enough user control.

Mitigation: Review the scheduled sync configuration, ~/.openclaw data, and iCloud Drive target folders before enabling automation.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/gzww/skills/openclaw-with-apple)
- [Artifact README](artifact/README.md)
- [Artifact security notes](artifact/SECURITY.md)
- [Artifact tutorial](artifact/TUTORIAL.md)
- [Apple ID account management](https://appleid.apple.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local task and note JSON files, calendar operations, iCloud Drive uploads, and Apple Health analysis reports when configured.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
