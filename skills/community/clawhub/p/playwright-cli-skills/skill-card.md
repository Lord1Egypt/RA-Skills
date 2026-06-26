## Description: <br>
Automate browser interactions, test web pages and work with Playwright tests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xinqian598188460](https://clawhub.ai/user/xinqian598188460) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to drive browser sessions with Playwright CLI, inspect pages, test flows, manage storage state, capture traces or videos, and generate Playwright-oriented commands or code. It also includes an Amazon product-search helper that exports top search results to CSV. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browser storage state, cookies, persistent profiles, traces, videos, screenshots, PDFs, and CSV exports may contain sensitive account or session data. <br>
Mitigation: Use a dedicated browser profile and low-risk test accounts; store generated artifacts securely and delete them when no longer needed. <br>
Risk: The Amazon search helper reuses a saved login session and writes product-search results locally. <br>
Mitigation: Avoid using a primary Amazon account; review the helper before execution and keep any saved auth file protected like a password. <br>
Risk: The skill can execute arbitrary Playwright code and browser actions through CLI commands. <br>
Mitigation: Review generated commands and code before running them, especially on authenticated, payment, or production sites. <br>


## Reference(s): <br>
- [Playwright Documentation](https://playwright.dev) <br>
- [Running Playwright Tests](references/playwright-tests.md) <br>
- [Request Mocking](references/request-mocking.md) <br>
- [Running Custom Playwright Code](references/running-code.md) <br>
- [Browser Session Management](references/session-management.md) <br>
- [Storage Management](references/storage-state.md) <br>
- [Test Generation](references/test-generation.md) <br>
- [Tracing](references/tracing.md) <br>
- [Video Recording](references/video-recording.md) <br>
- [Inspecting Element Attributes](references/element-attributes.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with inline shell commands, Playwright CLI commands, JavaScript snippets, YAML snapshots, screenshots, PDFs, traces, videos, and CSV files where workflows request them.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read and write browser storage state, persistent profiles, traces, videos, screenshots, PDFs, snapshots, and CSV exports.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
