## Description:

iFinD MCP helps agents query A-share stock, public fund, macroeconomic, and news information through iFinD financial-data MCP services.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xingjianliu0417](https://clawhub.ai/user/xingjianliu0417)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to configure and call iFinD MCP services for Chinese equity, fund, macroeconomic, and company-news queries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on a third-party global mcporter install.

Mitigation: Verify the mcporter package source, consider pinning a reviewed version, and avoid installing or running it with unnecessary privileges.

Risk: The iFinD bearer token can expose authorized financial-data access if leaked.

Mitigation: Store ~/.openclaw/mcporter.json with owner-only permissions, never commit or share the token, and revoke or rotate it if exposure is suspected.

## Reference(s):

- [iFinD MCP API Reference](references/API.md)
- [ClawHub skill page](https://clawhub.ai/xingjianliu0417/skills/ifind-mcp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-provided iFinD bearer token and mcporter configuration.]

## Skill Version(s):

1.3.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
