## Description: <br>
Chrome DevTools MCP gives agents browser automation and testing capabilities through Puppeteer and the Chrome DevTools Protocol, including navigation, form input, screenshots, performance traces, network inspection, and console debugging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[banalit](https://clawhub.ai/user/banalit) <br>

### License/Terms of Use: <br>
Apache-2.0 <br>


## Use Case: <br>
Developers and QA engineers use this skill to connect an agent to Chrome for browser automation, UI testing, visual checks, performance analysis, debugging, and network inspection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The MCP server can control and inspect Chrome, including pages where sensitive accounts or data may be present. <br>
Mitigation: Use a fresh or disposable browser profile, avoid sensitive logged-in sessions unless intended, and review actions before submissions or file uploads. <br>
Risk: The upstream Chrome DevTools MCP package may collect usage statistics by default and performance tools may use CrUX-related behavior. <br>
Mitigation: Use the documented privacy flags such as --no-usage-statistics and --no-performance-crux when that data sharing is not appropriate. <br>


## Reference(s): <br>
- [Chrome DevTools MCP homepage](https://github.com/ChromeDevTools/chrome-devtools-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON configuration snippets and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include OpenClaw MCP server configuration and setup, status, or test commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
