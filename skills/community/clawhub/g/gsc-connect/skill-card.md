## Description:

Connect OpenClaw or another MCP-compatible agent to Google Search Console and retrieve official read-only properties, performance, sitemap, and URL inspection data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[2winter-dev](https://clawhub.ai/user/2winter-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, site owners, and SEO practitioners use this skill to connect an MCP-compatible agent to Google Search Console for read-only performance, sitemap, property, and URL inspection workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill connects to a third-party remote MCP service that receives read-only Google Search Console authorization.

Mitigation: Confirm trust in the YUSIHK service before installation and grant only the documented read-only Search Console access.

Risk: Users may accidentally expose Google credentials, OAuth secrets, tokens, cookies, or authorization codes while configuring the connector.

Mitigation: Do not paste passwords, tokens, cookies, client secrets, or authorization codes into chat or configuration fields; use the documented OAuth flow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/2winter-dev/skills/gsc-connect)
- [YUSIHK product guide](https://yusihk.com/en/gsc-connect-codex-plugin-google-search-console/)
- [GSC Connect documentation](https://gsc.yusihk.com/docs)
- [GSC Connect Traditional Chinese documentation](https://gsc.yusihk.com/zh-hant/docs)
- [GSC Connect MCP endpoint](https://gsc.yusihk.com/mcp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, configuration values, and read-only workflow guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces guidance for connecting to a remote read-only MCP service and interpreting Google Search Console API results.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
