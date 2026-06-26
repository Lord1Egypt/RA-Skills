## Description: <br>
Browser automation via Playwright MCP server. Navigate websites, click elements, fill forms, extract data, take screenshots, and perform full browser automation workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[itsjustFred](https://clawhub.ai/user/itsjustFred) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to let an agent control a Playwright MCP browser session for website navigation, form interaction, data extraction, screenshots, and related browser automation tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browser automation may navigate to untrusted sites or perform account-changing actions. <br>
Mitigation: Use host allowlists or blocked-origin settings where possible, and review submissions or account-changing actions before they run. <br>
Risk: Credentials and saved browser outputs such as screenshots, traces, videos, and extracted page data may contain sensitive information. <br>
Mitigation: Avoid entering real credentials except on trusted sites, and treat generated browser artifacts and extracted page data as sensitive. <br>
Risk: Relaxed browser security options such as ignoring HTTPS errors or disabling sandboxing can increase exposure. <br>
Mitigation: Use relaxed security flags only for trusted testing scenarios and keep default sandboxing and host validation enabled for normal use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/itsjustFred/playwright-mcp-1-0-0) <br>
- [Playwright Docs](https://playwright.dev) <br>
- [Model Context Protocol](https://modelcontextprotocol.io) <br>
- [NPM Package: @playwright/mcp](https://www.npmjs.com/package/@playwright/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown with inline bash, Python, and MCP tool-call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill guides browser automation workflows and may produce or reference screenshots, traces, videos, and extracted page data through Playwright MCP.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
