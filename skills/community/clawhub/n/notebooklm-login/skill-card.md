## Description:

Logs in to Google NotebookLM via Chrome DevTools Protocol and saves authentication cookies for notebooklm-mcp when credentials are missing or expired.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ou-rock](https://clawhub.ai/user/ou-rock)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to authenticate Google NotebookLM for the notebooklm-mcp CLI or MCP server, especially when the standard login check reports missing or expired credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates and stores reusable Google/NotebookLM session material that can grant account access until revoked or expired.

Mitigation: Use only in a trusted local environment, protect the notebooklm-mcp profile directory, and revoke or delete stale saved cookies when access is no longer needed.

Risk: The browser-debugging setup and temporary Chromium profile can leave session material exposed after login.

Mitigation: Avoid running as root, delete stale /tmp/nlm-chrome-profile data, and stop any Chrome process using port 9222 after use.

Risk: Runtime dependencies and the login workflow should be reviewed before installation.

Mitigation: Pin and review dependencies before use, and scan the skill before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ou-rock/skills/notebooklm-login)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and troubleshooting guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires chromium-browser and uv; saves reusable Google/NotebookLM session cookies and metadata to the local notebooklm-mcp profile.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
