## Description: <br>
Browser automation guidance for using Playwright directly to navigate sites, interact with elements, extract data, capture screenshots or PDFs, record videos, and automate workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Spiceman161](https://clawhub.ai/user/Spiceman161) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to guide direct Playwright browser automation for web navigation, UI interaction, data extraction, screenshots, PDFs, video recording, and workflow automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan reports that the skill asks users to create persistent passwordless root permissions for Playwright install commands. <br>
Mitigation: Do not install the suggested sudoers rule; review and run any required Playwright dependency installation manually, then remove temporary elevation afterward. <br>
Risk: Browser automation outputs such as screenshots, recordings, downloads, cookies, and storageState files may contain account data or session tokens. <br>
Mitigation: Treat generated browser artifacts as sensitive, store them only where needed, and avoid sharing or persisting session material unnecessarily. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Spiceman161/playwright-browser-automation) <br>
- [Playwright Docs](https://playwright.dev) <br>
- [Playwright API Reference](https://playwright.dev/docs/api/class-playwright) <br>
- [Playwright Best Practices](https://playwright.dev/docs/best-practices) <br>
- [Playwright Locators Guide](https://playwright.dev/docs/locators) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline JavaScript, Python, and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and npx; generated browser artifacts such as screenshots, PDFs, videos, downloads, cookies, and storage state may contain sensitive data.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
