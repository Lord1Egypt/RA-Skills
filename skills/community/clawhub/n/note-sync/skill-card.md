## Description: <br>
Append notes to local Markdown files via MCP append_note. Use when the user asks to save ideas, reminders, or journal entries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lgwventrue](https://clawhub.ai/user/lgwventrue) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and ClawHub users use this skill to let an agent save selected chat content, reminders, and journal-style notes into local Markdown files through an MCP append_note tool. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill writes selected chat content to local Markdown files on disk, which can retain sensitive data if the user asks to save it. <br>
Mitigation: Avoid saving passwords, API keys, private messages, or sensitive personal data unless local disk retention is acceptable. <br>
Risk: The skill launches an external MCP executable from NOTE_SYNC_REPO. <br>
Mitigation: Review the external go-note-sync-mcp repository and built executable before configuring the MCP server. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/lgwventrue/note-sync) <br>
- [Setup Guide](artifact/references/setup.md) <br>
- [append_note tool reference](artifact/references/tool-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown notes and concise agent confirmation text, with setup guidance that includes shell commands and JSON configuration snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The append_note tool writes user-provided note content to local Markdown files under the configured NOTE_SYNC_REPO path.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter says 1.0.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
