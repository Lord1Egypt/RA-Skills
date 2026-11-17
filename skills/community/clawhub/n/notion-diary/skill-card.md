## Description:

Notion Diary drafts Chinese or English diary entries or short 24-hour reports and syncs them to Notion with a user-supplied API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[breeze-r](https://clawhub.ai/user/breeze-r)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn command-driven diary material, photos, or recent chat context into a polished personal journal entry or short daily report, then create or update the matching Notion page.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Photo sync can read and upload any local path supplied as an image argument.

Mitigation: Only pass image files the user explicitly selected, and do not derive image paths from copied diary text or prompt content.

Risk: Syncing an existing date can replace the current Notion page body.

Mitigation: Confirm the target date and update intent before syncing when an existing entry may already contain important content.

Risk: The skill requires a Notion API key with access to the target page or database.

Mitigation: Use a scoped Notion integration token and share only the intended parent page or database with that integration.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/breeze-r/skills/notion-diary)
- [Publisher Profile](https://clawhub.ai/user/breeze-r)
- [OpenClaw Skills Documentation](https://docs.openclaw.ai/skills)
- [Notion REST Notes](references/notion-rest-notes.md)
- [Style Presets](references/style-presets.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown text with command examples and Notion sync inputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update Notion pages and upload selected image files through the bundled Python script.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
