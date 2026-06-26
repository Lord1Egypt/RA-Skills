## Description: <br>
Browser automation using the Playwright API directly for website navigation, element interaction, data extraction, screenshots, PDFs, video recording, and complex workflow automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[onlyloveher](https://clawhub.ai/user/onlyloveher) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation engineers use this skill to guide browser automation with Playwright for navigation, interaction, form workflows, data extraction, screenshots, PDFs, video recording, and debugging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes examples for stored authentication sessions and credentials, which can expose sensitive access if written to shared or persistent locations. <br>
Mitigation: Use isolated browser contexts and test accounts where possible; avoid storing real credentials or auth.json unless necessary; delete sensitive session files promptly. <br>
Risk: Screenshots, PDFs, videos, traces, and downloads may capture private data from automated browser sessions. <br>
Mitigation: Keep captures and downloads in access-controlled locations and remove sensitive outputs after review. <br>
Risk: The sudoers setup example grants passwordless execution for Playwright dependency installation commands. <br>
Mitigation: Do not add passwordless sudoers rules unless the local privilege risk is understood and accepted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/onlyloveher/playwright-automation-v1) <br>
- [Playwright Docs](https://playwright.dev) <br>
- [Playwright API Reference](https://playwright.dev/docs/api/class-playwright) <br>
- [Playwright Best Practices](https://playwright.dev/docs/best-practices) <br>
- [Playwright Locators Guide](https://playwright.dev/docs/locators) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JavaScript and shell code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include commands that install browsers or system dependencies and examples that create screenshots, PDFs, videos, traces, downloads, or stored authentication state.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
