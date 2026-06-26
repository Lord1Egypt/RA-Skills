## Description: <br>
Browser automation via Playwright MCP server. Navigate websites, click elements, fill forms, extract data, take screenshots, and perform full browser automation workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Spiceman161](https://clawhub.ai/user/Spiceman161) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and automation-focused agents use this skill to control a browser through Playwright MCP for navigation, form interaction, data extraction, screenshots, and browser workflow testing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browser automation can interact with logged-in sites, submit forms, upload files, make purchases, change settings, or run page JavaScript. <br>
Mitigation: Use host allow-lists, avoid unsupervised use on logged-in or high-value accounts, and review actions that submit data, upload files, make purchases, change settings, or execute page JavaScript. <br>
Risk: The skill depends on Playwright MCP and npx being installed and available in the execution environment. <br>
Mitigation: Confirm the required binaries before use and install @playwright/mcp and the needed Playwright browsers according to the documented installation steps. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Spiceman161/playwright-mcp) <br>
- [Publisher profile](https://clawhub.ai/user/Spiceman161) <br>
- [Playwright documentation](https://playwright.dev) <br>
- [Model Context Protocol](https://modelcontextprotocol.io) <br>
- [NPM package: @playwright/mcp](https://www.npmjs.com/package/@playwright/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands, MCP tool call examples, and Python example code] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide browser actions that save screenshots, traces, or videos when Playwright MCP output options are configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
