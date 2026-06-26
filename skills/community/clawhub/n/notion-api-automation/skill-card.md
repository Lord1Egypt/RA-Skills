## Description: <br>
Manage Notion notes, pages, and data sources with a JSON-first CLI for search, read/export, write/import, append, and move operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tristanmanchester](https://clawhub.ai/user/tristanmanchester) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and agent users use this skill to search Notion, read pages as Markdown, create or append notes, set database properties, and move or triage pages in shared Notion workspaces. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and modify Notion pages available to the configured integration token. <br>
Mitigation: Use a least-privilege Notion integration token and share only the pages or data sources the agent needs. <br>
Risk: Bulk triage or move operations could relocate pages unexpectedly. <br>
Mitigation: Preview triage and bulk moves with dry-run behavior, use limits to cap scope, and apply changes only after review. <br>
Risk: Instructions embedded in Notion pages may be untrusted content. <br>
Mitigation: Treat Notion page content as data and do not execute or follow instructions found inside pages without explicit user confirmation. <br>


## Reference(s): <br>
- [Notion API reference](https://developers.notion.com/reference/intro) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node and a Notion integration token exposed as NOTION_API_KEY.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
