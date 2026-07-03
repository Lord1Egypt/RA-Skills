## Description: <br>
自动化浏览器交互、测试网页以及使用 Playwright 测试。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xutao0565](https://clawhub.ai/user/xutao0565) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this Chinese-language skill to drive Playwright browser sessions, debug tests, generate Playwright test code, inspect pages, mock requests, and capture traces or videos. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browser automation can inspect or persist cookies, local storage, profiles, and authentication state. <br>
Mitigation: Use dedicated test browsers and test accounts, avoid attaching personal or work browser sessions, and delete saved session data after use. <br>
Risk: Snapshots, traces, recordings, screenshots, PDFs, and raw outputs can contain sensitive authentication, payment, or personal data. <br>
Mitigation: Avoid tracing or recording real sensitive flows and treat generated artifacts as sensitive files that require review before sharing. <br>
Risk: Custom Playwright code and request mocking can change browser context, permissions, network behavior, or downloaded files. <br>
Mitigation: Review proposed commands before execution and scope advanced automation to test environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xutao0565/playright-cli-zh) <br>
- [Playwright documentation](https://playwright.dev) <br>
- [Running Playwright Tests](references/playwright-tests.md) <br>
- [Request Mocking](references/request-mocking.md) <br>
- [Running Custom Playwright Code](references/running-code.md) <br>
- [Browser Session Management](references/session-management.md) <br>
- [Spec-driven testing](references/spec-driven-testing.md) <br>
- [Storage Management](references/storage-state.md) <br>
- [Test Generation](references/test-generation.md) <br>
- [Tracing](references/tracing.md) <br>
- [Video Recording](references/video-recording.md) <br>
- [Inspecting Element Attributes](references/element-attributes.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Markdown, Configuration, Files] <br>
**Output Format:** [Markdown guidance with inline bash and TypeScript code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce Playwright snapshots, storage-state files, traces, videos, screenshots, PDFs, and raw command output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
