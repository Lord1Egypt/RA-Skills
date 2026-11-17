## Description:

Automates browser interaction, web page testing, and Playwright test workflows through playwright-cli.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xutao0565](https://clawhub.ai/user/xutao0565)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and QA engineers use this skill to drive browser sessions, inspect page state, generate locators and tests, mock requests, and debug Playwright flows from an agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad browser automation can access, save, or alter sensitive browser session data.

Mitigation: Use test accounts where possible, avoid real payment or secret-bearing flows, do not print or persist cookies or tokens unless necessary, and delete auth-state files after use.

Risk: Tracing and video recording can persist sensitive page content or user data.

Mitigation: Avoid capturing real secrets, personal data, or payment flows; review generated traces and videos before sharing or retaining them.

Risk: The installation guidance allows mutable npm tooling through latest or global installs.

Mitigation: Prefer pinned project-local npm dependencies over global latest installs.

## Reference(s):

- [Playwright documentation](https://playwright.dev)
- [Inspecting Element Attributes](references/element-attributes.md)
- [Running Playwright Tests](references/playwright-tests.md)
- [Request Mocking](references/request-mocking.md)
- [Running Custom Playwright Code](references/running-code.md)
- [Browser Session Management](references/session-management.md)
- [Spec-driven testing](references/spec-driven-testing.md)
- [Storage Management](references/storage-state.md)
- [Test Generation](references/test-generation.md)
- [Tracing](references/tracing.md)
- [Video Recording](references/video-recording.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and Playwright TypeScript snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May also guide creation of browser state files, screenshots, PDFs, traces, and video recordings through playwright-cli commands.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
