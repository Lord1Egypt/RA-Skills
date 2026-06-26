## Description: <br>
Browser automation via Playwright MCP server. Navigate websites, click elements, fill forms, extract data, take screenshots, and perform full browser automation workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ramspan](https://clawhub.ai/user/ramspan) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and QA engineers use this skill to let an agent control Playwright MCP for browser navigation, form interaction, web data extraction, screenshots, and browser workflow automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browser automation can navigate untrusted sites or submit forms and file uploads on behalf of an agent. <br>
Mitigation: Use allowed-host settings for trusted domains and review form submissions and file uploads before running them. <br>
Risk: Screenshots, traces, videos, and browser output may contain sensitive page data. <br>
Mitigation: Disable trace and video capture unless needed, avoid entering secrets on untrusted sites, and store browser outputs only in approved locations. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ramspan/pascal-playwright-mcp) <br>
- [Playwright Documentation](https://playwright.dev) <br>
- [Model Context Protocol](https://modelcontextprotocol.io) <br>
- [Playwright MCP NPM Package](https://www.npmjs.com/package/@playwright/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash commands, JSON-like MCP tool-call examples, and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or reference browser output files such as screenshots, traces, and videos when those options are enabled.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
