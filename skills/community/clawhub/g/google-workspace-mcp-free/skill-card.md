## Description: <br>
Provides agent guidance for using @presto-ai/google-workspace-mcp to access basic Gmail, Calendar, Drive, Docs, Sheets, Time, and Auth workflows through OAuth-based Google Workspace tooling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users can use this skill to configure and call Google Workspace MCP tools for personal productivity tasks such as searching mail, reviewing calendars, finding Drive files, extracting document text, and reading spreadsheet ranges. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The install path may expose broader Google account permissions and write-capable tools than the free read-focused description makes clear. <br>
Mitigation: Before authorization, inspect the OAuth consent screen and granted scopes, and proceed only with scopes acceptable for the account being connected. <br>
Risk: A personal or production Google account could expose sensitive mail, calendar, Drive, Docs, or Sheets data to a third-party MCP server. <br>
Mitigation: Use a dedicated test account or tightly controlled Workspace account, and avoid authorizing accounts containing data that should not be exposed to this integration. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/google-workspace-mcp-free) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance is centered on OAuth authorization and mcporter calls to the google-workspace MCP server.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
