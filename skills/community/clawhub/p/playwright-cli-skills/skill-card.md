## Description:

Automate browser interactions, test web pages, and work with Playwright tests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xinqian598188460](https://clawhub.ai/user/xinqian598188460)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and QA engineers use this skill to drive Playwright CLI browser sessions, inspect web pages, debug Playwright tests, manage browser state, mock requests, capture traces or videos, and generate automation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad browser-control commands can interact with authenticated sites and sensitive browser state.

Mitigation: Use isolated test accounts and sessions, review proposed browser actions, and close or delete session data after use.

Risk: Saved browser storage can contain credentials or session tokens.

Mitigation: Treat storage-state files as secrets, store them outside shared workspaces, and remove them when no longer needed.

Risk: The bundled Amazon helper uses saved Amazon login state and writes untrusted product data to CSV files.

Mitigation: Review the helper before execution, avoid payment or production shopping accounts, and validate CSV output before importing it elsewhere.

Risk: Global npm installation guidance can introduce unpinned tool versions.

Mitigation: Prefer a locally pinned dependency or confirm the exact package version before installing or running the CLI.

## Reference(s):

- [Playwright documentation](https://playwright.dev)
- [Element attributes](references/element-attributes.md)
- [Running Playwright tests](references/playwright-tests.md)
- [Request mocking](references/request-mocking.md)
- [Running custom Playwright code](references/running-code.md)
- [Browser session management](references/session-management.md)
- [Storage management](references/storage-state.md)
- [Test generation](references/test-generation.md)
- [Tracing](references/tracing.md)
- [Video recording](references/video-recording.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, Playwright code snippets, configuration examples, and generated file paths.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce browser snapshots, screenshots, PDFs, traces, videos, storage-state files, and CSV reports when the referenced CLI commands or helper scripts are executed.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
