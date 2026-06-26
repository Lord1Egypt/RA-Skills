## Description: <br>
Use when the user asks to browse, upload, download, share, or manage Google Drive files and folders through the gogcli Google Drive MCP server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chrischall](https://clawhub.ai/user/chrischall) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to configure and operate a Google Drive MCP server for browsing, uploading, downloading, sharing, and managing Drive files, folders, permissions, shared drives, and comments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The configured MCP server can affect Google Drive files, sharing, permissions, and comments for the selected account. <br>
Mitigation: Before approving actions, verify the exact file or folder, destination, permission target, and operation, especially for delete, move, replace, share, unshare, or comment changes. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/chrischall/gogcli-mcp-drive) <br>
- [gogcli project](https://github.com/openclaw/gogcli) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, Shell commands] <br>
**Output Format:** [Markdown with JSON configuration blocks and inline tool names] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires gogcli to be installed and authenticated, Node.js 18 or later, and a configured GOG_ACCOUNT for the selected Google account.] <br>

## Skill Version(s): <br>
2.8.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
