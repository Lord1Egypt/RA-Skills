## Description:

Browser automation using Playwright API directly for navigation, interaction, data extraction, screenshots, PDFs, video recording, and complex workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[onlyloveher](https://clawhub.ai/user/onlyloveher)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation engineers use this skill to guide Playwright-based browser automation for web testing, data extraction, page capture, and workflow scripting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact includes sudoers guidance that would grant passwordless root access for broad npx Playwright commands.

Mitigation: Do not copy the sudoers setup; use pinned Playwright versions and have administrators install system dependencies as a one-time managed step.

Risk: Browser automation can create screenshots, videos, traces, downloads, cookies, localStorage, and auth state files that contain sensitive information.

Mitigation: Treat browser artifacts as sensitive, store them securely, avoid committing them, and remove them when they are no longer needed.

Risk: Automating logged-in accounts can expose session data through cookies, localStorage, or auth.json files.

Mitigation: Use least-privilege test accounts where possible and handle saved authentication state as secret material.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/onlyloveher/skills/playwright-automation-v1)
- [Playwright Docs](https://playwright.dev)
- [Playwright API Reference](https://playwright.dev/docs/api/class-playwright)
- [Playwright Best Practices](https://playwright.dev/docs/best-practices)
- [Playwright Locators Guide](https://playwright.dev/docs/locators)
- [Playwright Trace Viewer](https://trace.playwright.dev)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, configuration]

**Output Format:** [Markdown with JavaScript, Python, and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May result in browser artifacts such as screenshots, PDFs, videos, traces, downloads, cookies, localStorage, or auth state files.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact/_meta.json reports 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
