## Description:

Access Granola AI meeting notes via MCP (mcporter), including meeting search, date-range listing, meeting details, verbatim transcripts, and OAuth token refresh after authentication failures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bholagabbar](https://clawhub.ai/user/bholagabbar)

### License/Terms of Use:


## Use Case:

Employees and external users with configured Granola MCP access use this skill to ask agents about meeting discussions, decisions, action items, and verbatim transcripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access private Granola meeting notes and transcripts through a bearer-token MCP configuration.

Mitigation: Install only for trusted publishers and restrict the Granola OAuth and mcporter configuration files to the owning user.

Risk: The token refresh script reads the token endpoint from local configuration before posting OAuth refresh data.

Mitigation: Hardcode or allowlist the Granola token endpoint before using token refresh.

Risk: The optional cron refresh path can repeatedly handle sensitive OAuth tokens before the refresh-script concerns are fixed.

Mitigation: Avoid enabling optional cron refresh until endpoint trust, response handling, and token interpolation issues are reviewed and corrected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bholagabbar/skills/granola-mcp)
- [Granola OAuth authorization endpoint](https://mcp-auth.granola.ai/oauth2/authorize)
- [Granola OAuth token endpoint](https://mcp-auth.granola.ai/oauth2/token)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with MCP tool-call guidance and inline shell commands; configuration is JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires mcporter, bash, curl, python3, and local Granola OAuth/MCP configuration files.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
