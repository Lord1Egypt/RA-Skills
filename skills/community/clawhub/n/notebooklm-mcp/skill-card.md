## Description:

Use when the user wants to configure, authenticate, or use Google NotebookLM via the nlm CLI or MCP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[afonsoft](https://clawhub.ai/user/afonsoft)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other NotebookLM users use this skill to set up the unofficial CLI or MCP server, authenticate their Google session, and manage notebooks and sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The unofficial client stores Google session cookies locally, which can grant access beyond NotebookLM.

Mitigation: Use a dedicated Google account, prefer desktop auto-login, never share cookie values in chat or logs, and delete cookies.txt immediately after import.

Risk: The setup helper can persistently change an unintended agent configuration when targeting one platform.

Mitigation: Review configuration changes before running the helper and avoid its --platform mode until platform matching and the legacy Devin exemption are fixed.

Risk: Notebook sources and prompts can contain sensitive information sent to Google.

Mitigation: Review content before adding it to notebooks and do not upload secrets, credentials, or personal information.

## Reference(s):

- [Authentication guide](references/auth-guide.md)
- [MCP configuration guide](references/mcp-config.md)
- [Platform quirks](references/platform-quirks.md)
- [Upstream authentication documentation](https://github.com/jacob-bd/notebooklm-mcp-cli/blob/main/docs/AUTHENTICATION.md)
- [Upstream MCP documentation](https://github.com/jacob-bd/notebooklm-mcp-cli/blob/main/docs/MCP_GUIDE.md)
- [Upstream CLI documentation](https://github.com/jacob-bd/notebooklm-mcp-cli/blob/main/docs/CLI_GUIDE.md)
- [NotebookLM MCP CLI package](https://pypi.org/project/notebooklm-mcp-cli/)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Instructions for authentication, setup, verification, and NotebookLM use]

## Skill Version(s):

1.0.9 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
