## Description:

Browser automation via Playwright MCP server. Navigate websites, click elements, fill forms, extract data, take screenshots, and perform full browser automation workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[itsjustfred](https://clawhub.ai/user/itsjustfred)

### License/Terms of Use:


## Use Case:

Developers and automation engineers use this skill to drive browser sessions through Playwright MCP for navigation, form interaction, data extraction, screenshots, and browser workflow automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned npm or npx execution can install or run a package version that differs from the reviewed release.

Mitigation: Pin and verify the exact @playwright/mcp package version before use, and prefer project-local installation over global installation.

Risk: Browser automation can control authenticated web sessions and interact with sensitive sites.

Mitigation: Run the skill in an isolated, unprivileged environment and configure allowed hosts before browsing.

Risk: Ignoring HTTPS errors can hide certificate or interception problems on unintended targets.

Mitigation: Use ignore-HTTPS-errors only for a clearly justified test target.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/itsjustfred/skills/playwright-mcp-1-0-0)
- [Playwright documentation](https://playwright.dev)
- [Model Context Protocol](https://modelcontextprotocol.io)
- [@playwright/mcp npm package](https://www.npmjs.com/package/@playwright/mcp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash, Python, and MCP call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes browser automation tool names, install commands, configuration options, and usage examples.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
