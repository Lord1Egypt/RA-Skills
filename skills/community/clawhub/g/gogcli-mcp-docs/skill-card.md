## Description: <br>
Helps agents read, edit, export, comment on, and manage Google Docs through the gogcli Docs MCP server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chrischall](https://clawhub.ai/user/chrischall) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to let Codex work with Google Docs for a configured Google account, including document reading, editing, exporting, tab management, and comments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read, edit, export, comment on, and trash Google Docs for the configured account. <br>
Mitigation: Install it only for intended Google Docs workflows, use explicit document IDs, and ask for previews or copies before bulk replace, delete, export, or trash actions. <br>
Risk: Markdown table conversion has documented formatting limitations for multiple tables, inline formatting inside table cells, and empty-header tables. <br>
Mitigation: Split large table appends into smaller calls, insert plain table-cell text before applying formatting, and supply non-empty header rows. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/chrischall/gogcli-mcp-docs) <br>
- [gogcli Project](https://github.com/openclaw/gogcli) <br>
- [gogcli-mcp Project Link](https://github.com/chrischall/gogcli-mcp) <br>
- [gogcli Issue 607](https://github.com/openclaw/gogcli/issues/607) <br>
- [gogcli Issue 608](https://github.com/openclaw/gogcli/issues/608) <br>
- [gogcli Issue 609](https://github.com/openclaw/gogcli/issues/609) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown and text responses with Google Docs MCP tool usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include document export formats such as PDF, TXT, HTML, DOCX, RTF, ODT, or EPUB when the underlying tool is used.] <br>

## Skill Version(s): <br>
2.8.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
