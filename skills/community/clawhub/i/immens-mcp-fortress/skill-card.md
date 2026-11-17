## Description:

Connect OpenClaw to any WordPress site running Immens MCP Fortress. Manage posts, pages, media, comments, users, WooCommerce, SEO, translations, and 274+ WordPress operations via MCP tools. Secure bearer-token authentication with SHA-256 hashed API keys, IP whitelisting, and rate limiting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[studioimmens](https://clawhub.ai/user/studioimmens)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and WordPress site operators use this skill to connect OpenClaw to WordPress sites running Immens MCP Fortress so an agent can manage content, users, media, WooCommerce, SEO, translations, and plugin integrations through MCP tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The connected agent can receive broad WordPress site-changing authority.

Mitigation: Install with a narrowly scoped WordPress Access Point and start on staging before production use.

Risk: Bearer API keys can grant site access if exposed in shared shells, logs, or chat transcripts.

Mitigation: Treat API keys like passwords, avoid pasting them into shared environments, and rotate any key that may have been exposed.

Risk: Deletes, user changes, WooCommerce changes, plugin settings, and Code Snippets operations can affect site integrity or customers.

Mitigation: Require human approval for sensitive or destructive operations and use IP allowlisting and audit logs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/studioimmens/skills/immens-mcp-fortress)
- [Repository](https://github.com/Studio-Immens/immens-mcp-fortress)
- [WordPress Plugin](https://wordpress.org/plugins/immens-mcp-fortress/)
- [Immens MCP Fortress Pro](https://studioimmens.com/immens-mcp-fortress-pro)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and MCP configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include bearer-token configuration details that should be handled as credentials.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
