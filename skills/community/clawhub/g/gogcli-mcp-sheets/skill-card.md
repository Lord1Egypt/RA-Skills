## Description: <br>
Helps an agent read, write, format, and manage Google Sheets through the gogcli Sheets MCP server, including authentication and spreadsheet operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chrischall](https://clawhub.ai/user/chrischall) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to configure and operate a Google Sheets MCP server for reading, editing, formatting, tab management, named ranges, exports, and other spreadsheet tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables spreadsheet-changing operations without enough scoping or confirmation guidance. <br>
Mitigation: Require explicit user confirmation before deleting tabs, overwriting ranges, changing structure or formatting, copying sheets, or exporting spreadsheet contents. <br>
Risk: Spreadsheet contents may include sensitive or business-critical data. <br>
Mitigation: Review the skill before installing and use it only when Google Sheets access is intended for the task. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chrischall/gogcli-mcp-sheets) <br>
- [gogcli project](https://github.com/openclaw/gogcli) <br>
- [gogcli-mcp repository referenced by artifact](https://github.com/chrischall/gogcli-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, shell commands] <br>
**Output Format:** [Markdown with JSON configuration snippets and tool guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js 18 or later and an installed, authenticated gogcli setup.] <br>

## Skill Version(s): <br>
2.8.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
