## Description: <br>
Write diary entries or short 24-hour reports in Chinese or English, then sync them into Notion using a user-supplied NOTION_API_KEY and the bundled Python script. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[breeze-r](https://clawhub.ai/user/breeze-r) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to draft personal diary entries or short daily reports from command input, conversation context, and optional photos, then sync the result to a Notion diary database. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Notion integration token and can create or update diary and report pages in the connected workspace. <br>
Mitigation: Use a dedicated Notion integration shared only with the intended diary page or database, and avoid broad workspace permissions. <br>
Risk: Syncing the same date again can replace existing Notion page body content. <br>
Mitigation: Review generated entries before syncing, use lookup or Notion history before re-syncing important dates, and keep a backup when preserving prior page content matters. <br>


## Reference(s): <br>
- [Notion REST Notes](references/notion-rest-notes.md) <br>
- [Style Presets](references/style-presets.md) <br>
- [OpenClaw Skills Documentation](https://docs.openclaw.ai/skills) <br>
- [OpenClaw Skill Tools Documentation](https://docs.openclaw.ai/tools/skills) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown diary or report text with optional shell command invocations for Notion sync] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-supplied NOTION_API_KEY to sync entries and optional photos to Notion.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
