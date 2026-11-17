## Description:

Browser automation using the Playwright API directly to navigate websites, interact with elements, extract data, take screenshots, generate PDFs, record videos, and automate complex workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spiceman161](https://clawhub.ai/user/spiceman161)

### License/Terms of Use:


## Use Case:

Developers and automation engineers use this skill to guide browser automation with Playwright, including navigation, interaction, data extraction, screenshots, PDFs, videos, authentication flows, and file transfer workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact includes privileged Playwright setup guidance that could create persistent passwordless root access.

Mitigation: Do not apply the sudoers instructions or run sudo npx; install Playwright through a pinned project dependency and perform browser setup in an isolated unprivileged environment.

Risk: Browser automation can create or process sensitive artifacts such as authentication state, traces, recordings, screenshots, downloads, and uploaded local files.

Mitigation: Treat those files as sensitive, store them only where needed, review them before sharing, and remove them after use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/spiceman161/skills/playwright-browser-automation)
- [Playwright Docs](https://playwright.dev)
- [Playwright API Reference](https://playwright.dev/docs/api/class-playwright)
- [Playwright Best Practices](https://playwright.dev/docs/best-practices)
- [Playwright Locators Guide](https://playwright.dev/docs/locators)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, code, shell commands, configuration]

**Output Format:** [Markdown with JavaScript, Python, JSON, and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce browser automation guidance that handles screenshots, PDFs, videos, traces, downloads, uploads, and authentication state files.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
