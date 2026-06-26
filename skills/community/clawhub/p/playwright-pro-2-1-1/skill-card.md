## Description: <br>
Production-grade Playwright testing toolkit for AI coding agents that generate tests, fix flaky failures, migrate Cypress or Selenium suites, sync with TestRail, run on BrowserStack, and produce reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thangcq0310](https://clawhub.ai/user/thangcq0310) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and test engineers use this skill to create, review, migrate, debug, and report Playwright end-to-end tests. It also helps coordinate optional TestRail and BrowserStack workflows when the user supplies the required account credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated tests and templates can mutate accounts, APIs, payment flows, password flows, account deletion, or lockout behavior. <br>
Mitigation: Run generated tests only against staging or isolated test tenants with disposable accounts and low-privilege secrets. <br>
Risk: TestRail and BrowserStack workflows can use real credentials and upload test cases, results, logs, videos, screenshots, or other test details to third-party services. <br>
Mitigation: Use scoped credentials, review each upload or sync step before execution, and avoid sending sensitive production data. <br>
Risk: Playwright storageState files, traces, screenshots, videos, and reports can contain secrets or session data. <br>
Mitigation: Keep storageState and test artifacts out of git and shared artifacts unless they have been reviewed and sanitized. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/thangcq0310/playwright-pro-2-1-1) <br>
- [README](README.md) <br>
- [Golden Rules](reference/golden-rules.md) <br>
- [Locator Guidance](reference/locators.md) <br>
- [Assertion Guidance](reference/assertions.md) <br>
- [Template Index](templates/README.md) <br>
- [BrowserStack account settings](https://www.browserstack.com/accounts/settings) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline code blocks, Playwright test code, shell commands, configuration snippets, and summary tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose files, commands, MCP actions, and third-party upload or sync steps that should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; artifact _meta.json lists 2.1.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
