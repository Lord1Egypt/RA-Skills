## Description:

Helps agents browse, upload, download, share, and manage Google Drive files and folders through a gogcli-based Drive MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill when an agent needs to work with Google Drive files, folders, shared drives, file permissions, and comments using authenticated Drive tooling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run an npm package with authenticated Google Drive access.

Mitigation: Pin the npm package to a reviewed version where possible, verify the package publisher and repository relationship, and use only an account and OAuth scopes appropriate for the files being managed.

Risk: Drive operations can delete, replace, move, share, unshare, download sensitive files, or change comments and permissions.

Mitigation: Require clear confirmation before destructive, sharing, permission, sensitive download, or comment-changing operations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chrischall/skills/gogcli-mcp-drive)
- [gogcli project](https://github.com/openclaw/gogcli)
- [gogcli MCP project](https://github.com/chrischall/gogcli-mcp)

## Skill Output:

**Output Type(s):** [guidance, configuration, shell commands]

**Output Format:** [Markdown with JSON configuration and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require Google account authentication and appropriate Drive OAuth scopes before use.]

## Skill Version(s):

2.8.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
