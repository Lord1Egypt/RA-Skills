## Description:

Playwright Browser Use provides a local Playwright-based browser automation CLI for opening pages, capturing snapshots, clicking, filling forms, managing tabs, handling cookies and storage, executing page JavaScript, and running Playwright code through a token-protected local daemon.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yicko](https://clawhub.ai/user/yicko)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to automate visible local browser workflows such as navigation, form entry, page inspection, screenshots, downloads, tab management, and controlled Playwright scripting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Default operation gives a local daemon token broad browser automation, page JavaScript execution, Playwright code execution, file upload or download, and persistent session authority.

Mitigation: Install only for trusted local use where the browser is visible and interruptible; prefer PW_BROWSER_SAFE_MODE=1 for agent-driven or untrusted-page workflows.

Risk: Cookie and storage commands can expose, export, import, clear, or set session credentials and authentication state.

Mitigation: Use PW_BROWSER_CRED_PERSIST=off when session files should never be written, avoid sensitive logged-in accounts, clear cookies and storage when finished, and shut down the daemon.

Risk: Untrusted automation targets can combine browser reachability with authenticated page state to submit actions or make credentialed requests.

Mitigation: Scope operations to user-approved pages, review proposed actions before execution, and add sandbox or network isolation when handling untrusted inputs.

## Reference(s):

- [English README](README.en.md)
- [English Quickstart](QUICKSTART.en.md)
- [Pagination Strategy](references/pagination.md)
- [Rich Text Editor Strategy](references/rich-text-editor.md)
- [Running Custom Code](references/running-code.md)
- [Node.js](https://nodejs.org/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline shell commands, plus CLI text or JSON responses and generated browser artifacts such as screenshots or downloads.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may reflect live browser state, authenticated sessions, local files selected for upload, and pages reachable from the user's machine.]

## Skill Version(s):

1.0.16 (source: server release metadata; artifact package.json and CHANGELOG report 1.3.11)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
