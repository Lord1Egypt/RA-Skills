## Description: <br>
Browser automation via remote Playwright WebSocket server for screenshots, PDFs and testing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[first-it-consulting](https://clawhub.ai/user/first-it-consulting) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to drive a trusted remote Playwright browser for screenshots, PDF export, and test execution without installing browsers locally. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The configured remote Playwright server can observe requested URLs, page contents, cookies available to the browser session, screenshots, PDFs, and test activity. <br>
Mitigation: Use only a Playwright WebSocket server that the user controls or fully trusts, and avoid sensitive or authenticated sites unless the server is authorized to process that data. <br>
Risk: The PLAYWRIGHT_WS endpoint may reveal private infrastructure or credentials if printed in logs or shared with an agent transcript. <br>
Mitigation: Keep the endpoint in environment configuration, do not echo its value, and rely on the release's redaction behavior for test output. <br>
Risk: Browser automation against live sites can capture or trigger unintended page behavior if targets and selectors are not reviewed. <br>
Mitigation: Review target URLs, selectors, and test commands before execution, especially when running against production or third-party services. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/first-it-consulting/playwright-ws) <br>
- [Selector Strategies](references/selectors.md) <br>
- [API Reference](references/api-reference.md) <br>
- [Playwright Documentation](https://playwright.dev/) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [PNG screenshots, PDF files, and terminal output from Node and Playwright commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and a PLAYWRIGHT_WS endpoint for a trusted remote Playwright server.] <br>

## Skill Version(s): <br>
1.0.3 (source: package.json, CHANGELOG, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
