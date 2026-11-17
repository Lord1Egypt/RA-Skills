## Description:

Browser automation via Playwright MCP server. Navigate websites, click elements, fill forms, extract data, take screenshots, and perform full browser automation workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ramspan](https://clawhub.ai/user/ramspan)

### License/Terms of Use:


## Use Case:

Developers and automation engineers use this skill to control browsers through Playwright MCP for navigation, form interaction, data extraction, screenshots, and browser workflow testing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and runs Playwright MCP through npm without pinned versions.

Mitigation: Review and pin the @playwright/mcp and playwright versions before installation, and avoid elevated privileges for global npm installs.

Risk: Browser automation can access untrusted hosts or bypass TLS validation if configured loosely.

Mitigation: Restrict allowed hosts, configure blocked origins where appropriate, and use --ignore-https-errors only in controlled testing.

Risk: Browser artifacts and extracted page content may contain sensitive information.

Mitigation: Treat screenshots, traces, videos, page snapshots, and extracted text as sensitive and store or share them only under the user's data-handling policy.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ramspan/skills/pascal-playwright-mcp)
- [Playwright documentation](https://playwright.dev)
- [Model Context Protocol](https://modelcontextprotocol.io)
- [NPM package @playwright/mcp](https://www.npmjs.com/package/@playwright/mcp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and MCP tool-call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce browser screenshots, traces, videos, page snapshots, and extracted page text when the configured MCP server is used.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
