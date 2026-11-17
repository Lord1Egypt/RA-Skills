## Description:

Automate browser interactions, test web pages and work with Playwright tests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zengzuo613](https://clawhub.ai/user/zengzuo613)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to control browser sessions, inspect pages, interact with UI elements, debug Playwright tests, and generate Playwright code from browser actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives an agent broad control over browser sessions and page state.

Mitigation: Install only when browser automation is intentional, avoid production accounts and real payment data, and review actions before using authenticated sessions.

Risk: The skill can inspect or modify cookies, localStorage, sessionStorage, profiles, and authentication state files.

Mitigation: Use isolated test accounts, delete or protect saved auth-state and profile files after use, and avoid storing sensitive credentials in browser state.

Risk: The documented global install path uses an unpinned latest package.

Mitigation: Prefer a project-local, lockfile-pinned Playwright CLI version before deploying the skill in repeatable workflows.

Risk: Screenshots, PDFs, traces, videos, downloads, and network captures may contain sensitive data.

Mitigation: Store generated artifacts only where intended, review them before sharing, and remove them when they are no longer needed.

## Reference(s):

- [Playwright documentation](https://playwright.dev)
- [Running Playwright Tests](artifact/references/playwright-tests.md)
- [Request Mocking](artifact/references/request-mocking.md)
- [Running Custom Playwright Code](artifact/references/running-code.md)
- [Browser Session Management](artifact/references/session-management.md)
- [Storage Management](artifact/references/storage-state.md)
- [Test Generation](artifact/references/test-generation.md)
- [Tracing](artifact/references/tracing.md)
- [Video Recording](artifact/references/video-recording.md)
- [Inspecting Element Attributes](artifact/references/element-attributes.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown with inline shell commands, Playwright snippets, and optional raw or JSON command output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create browser state, screenshot, PDF, trace, video, profile, and download files when commands request them.]

## Skill Version(s):

0.1.9 (source: artifact CHANGELOG.md and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
