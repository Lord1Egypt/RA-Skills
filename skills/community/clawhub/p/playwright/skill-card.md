## Description:

Helps agents write, repair, debug, and operate Playwright browser automation, tests, MCP browser sessions, CI runs, and JS-rendered page extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, QA engineers, and automation-focused agents use this skill to create or repair Playwright tests and scripts, diagnose flaky browser failures, configure CI runs, control browsers through Playwright MCP, and extract data from pages that require JavaScript rendering.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned Playwright or MCP package versions can change browser behavior or installed tooling unexpectedly.

Mitigation: Pin Playwright and MCP package versions or use a project lockfile before installation and CI use.

Risk: Credentialed browser sessions and auth artifacts can expose live access if reused or stored broadly.

Mitigation: Use isolated browser profiles for credentialed work and keep .auth files out of git and shared storage.

Risk: Traces, HARs, videos, and CI reports can contain tokens, cookies, page content, or personal data.

Mitigation: Keep these artifacts out of git and shared storage, and restrict CI artifact access and retention.

Risk: Browser automation can trigger production, paid, or destructive flows.

Mitigation: Require explicit user approval before automating production, payment, email-send, deletion, or other destructive flows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/playwright)
- [Clawic skill homepage](https://clawic.com/skills/playwright)
- [Playwright npm package](https://registry.npmjs.org/playwright)
- [Playwright MCP npm package](https://registry.npmjs.org/@playwright/mcp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline TypeScript, JavaScript, shell commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose Playwright specs, fixtures, configuration files, CI commands, MCP commands, debugging steps, and scraping patterns.]

## Skill Version(s):

1.0.4 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
