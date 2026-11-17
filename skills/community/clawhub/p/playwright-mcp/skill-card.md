## Description:

Browser automation via Playwright MCP server. Navigate websites, click elements, fill forms, extract data, take screenshots, and perform full browser automation workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spiceman161](https://clawhub.ai/user/spiceman161)

### License/Terms of Use:


## Use Case:

Developers and automation engineers use this skill to configure and operate the Playwright MCP server for browser navigation, form interaction, data extraction, screenshots, and browser automation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run mutable npm packages for a powerful browser-control MCP server.

Mitigation: Review before installing, prefer pinned package versions or a locked local install, and scan the skill before deployment.

Risk: Browser automation can navigate to untrusted sites or weaken transport validation when misconfigured.

Mitigation: Use allowed-hosts for trusted sites and avoid --ignore-https-errors except in controlled testing.

Risk: Saved screenshots, traces, videos, and form entries can contain sensitive information.

Mitigation: Treat generated browser artifacts and submitted form data as sensitive and apply appropriate retention and access controls.

## Reference(s):

- [Playwright Docs](https://playwright.dev)
- [MCP Protocol](https://modelcontextprotocol.io)
- [NPM Package: @playwright/mcp](https://www.npmjs.com/package/@playwright/mcp)
- [ClawHub Skill Page](https://clawhub.ai/spiceman161/skills/playwright-mcp)
- [Publisher Profile](https://clawhub.ai/user/spiceman161)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands, MCP tool examples, and Python example code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide agents to create browser screenshots, traces, videos, and extracted page data when configured through Playwright MCP.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
