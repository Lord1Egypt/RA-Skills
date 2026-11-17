## Description:

Browser automation via Playwright MCP for navigating websites, clicking elements, filling forms, taking screenshots, extracting rendered data, authoring Playwright tests, and debugging real browser workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhichengsong](https://clawhub.ai/user/zhichengsong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to plan and execute browser-driven testing, debugging, screenshots, downloads, form automation, and structured extraction when static HTTP fetches are insufficient.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing Playwright or Playwright MCP through npm can execute dependency code and may drift when dependencies are not pinned.

Mitigation: Install only in trusted projects, pin Playwright and Playwright MCP as project dependencies, commit a lockfile, and run local binaries through the project package manager.

Risk: Browser automation sends requests, form input, cookies, uploads, and page interactions to user-requested websites.

Mitigation: Automate only trusted or intended sites, keep browser auth state temporary unless reuse is explicitly required, and avoid unnecessary screenshots, traces, or downloads containing sensitive data.

Risk: Production, destructive, financial, medical, or other high-stakes account actions can have real-world impact if automated without confirmation.

Mitigation: Prefer staging or local environments for high-stakes flows and require explicit user confirmation before continuing with production actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhichengsong/skills/playwright-tmp)
- [Artifact homepage](https://clawic.com/skills/playwright)
- [Selector Strategies](artifact/selectors.md)
- [Debugging Guide](artifact/debugging.md)
- [Testing Patterns](artifact/testing.md)
- [CI Success Defaults](artifact/ci-cd.md)
- [Rendered-Page Extraction Patterns](artifact/scraping.md)
- [npm registry](https://registry.npmjs.org)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and Playwright JavaScript or TypeScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe browser actions, selectors, test configuration, CI setup, screenshots, traces, downloads, and rendered-page extraction workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
