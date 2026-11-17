## Description:

Browser automation using Playwright API directly to navigate websites, interact with elements, extract data, take screenshots, generate PDFs, record videos, and automate complex workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[manikantasai1987](https://clawhub.ai/user/manikantasai1987)

### License/Terms of Use:


## Use Case:

Developers and automation engineers use this skill to create Playwright-based browser workflows for navigation, interaction, data extraction, screenshots, PDFs, video recording, and browser configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent passwordless root access for broad npx Playwright commands can expand privilege and supply-chain exposure.

Mitigation: Avoid sudoers NOPASSWD rules, do not run unpinned npx commands as root, and pin Playwright through a locked project dependency.

Risk: Browser automation can create sensitive screenshots, videos, downloads, cookies, tokens, or saved authentication state.

Mitigation: Protect generated artifacts and authentication state files, restrict their retention and access, and review outputs before sharing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/manikantasai1987/skills/manikantasai-playwright-automation)
- [Playwright Docs](https://playwright.dev)
- [Playwright API Reference](https://playwright.dev/docs/api/class-playwright)
- [Playwright Best Practices](https://playwright.dev/docs/best-practices)
- [Playwright Locators Guide](https://playwright.dev/docs/locators)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript, Python, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include browser automation patterns, install commands, locator guidance, authentication examples, and artifact-handling guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
