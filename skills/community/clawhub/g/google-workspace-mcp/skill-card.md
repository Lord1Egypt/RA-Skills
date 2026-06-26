## Description: <br>
Gmail, Calendar, Drive, Docs, and Sheets access through OAuth sign-in without Google Cloud Console setup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dru-ca](https://clawhub.ai/user/dru-ca) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and Workspace users use this skill to install and call a Google Workspace MCP server with mcporter, then search, read, create, update, send, and manage content across Gmail, Calendar, Drive, Docs, Sheets, Slides, Chat, People, and time tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs an unpinned third-party MCP server with persistent OAuth access to Google Workspace data. <br>
Mitigation: Install only after trusting the @presto-ai npm package, verify OAuth consent scopes during sign-in, and use the least-privileged Google account practical. <br>
Risk: The available tools can send messages, change documents, modify Gmail or Calendar data, or delete data. <br>
Mitigation: Require explicit confirmation before any send, modify, or delete action and review the requested operation before execution. <br>
Risk: OAuth credentials persist locally after setup. <br>
Mitigation: Remove ~/.config/google-workspace-mcp/ and revoke the Google app when the skill is no longer used. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/dru-ca/google-workspace-mcp) <br>
- [Publisher profile](https://clawhub.ai/user/dru-ca) <br>
- [Skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash commands and mcporter examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides installation, OAuth re-authentication, credential deletion, and Google Workspace MCP tool calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
