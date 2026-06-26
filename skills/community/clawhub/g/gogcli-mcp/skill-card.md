## Description: <br>
This skill helps agents configure and use gogcli-backed MCP servers for Google Workspace automation across Docs, Sheets, Slides, Drive, and Classroom. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chrischall](https://clawhub.ai/user/chrischall) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and users who connect agents to Google Workspace use this skill to install and configure gogcli MCP servers for document, spreadsheet, presentation, file, and Classroom workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can enable broad Google Workspace actions through the user's gogcli account. <br>
Mitigation: Install only for intended Google Workspace automation, use the least-privileged Google account possible, and scope GOG_ACCOUNT explicitly when multiple accounts exist. <br>
Risk: Workspace edits, sharing changes, deletions, grade changes, and Classroom operations can affect real user data. <br>
Mitigation: Require explicit confirmation before sensitive actions and verify document, file, course, and assignment IDs before execution. <br>
Risk: Server security evidence flags the release as suspicious because of broad scope and limited safety guidance. <br>
Mitigation: Review the skill before installation and apply the server guidance for confirmations and least-privilege account use. <br>


## Reference(s): <br>
- [gogcli GitHub repository](https://github.com/chrischall/gogcli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON configuration examples and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes MCP server configuration, gogcli authentication guidance, and package selection guidance.] <br>

## Skill Version(s): <br>
2.10.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
