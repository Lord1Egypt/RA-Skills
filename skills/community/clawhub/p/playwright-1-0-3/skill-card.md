## Description:

Browser automation via Playwright MCP for navigating websites, clicking elements, filling forms, taking screenshots, extracting data, debugging browser workflows, and authoring Playwright tests or scripts when static fetch is insufficient.

This skill is ready for commercial/non-commercial use.

## Publisher:

[howerlin0329](https://clawhub.ai/user/howerlin0329)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to plan and execute browser automation with Playwright MCP, direct Playwright scripts, and Playwright tests for rendered UI workflows, screenshots, PDFs, downloads, debugging, CI, selector strategy, and bounded rendered-page extraction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing Playwright or Playwright MCP can fetch npm package metadata and tarballs, and unpinned installs can drift over time.

Mitigation: Prefer a project-local Playwright dependency with a committed lockfile and run npm ci in sensitive repositories or CI.

Risk: Browser automation can send form input, cookies, uploads, and page interactions to user-requested web origins.

Mitigation: Run against intended local, staging, or authorized targets and avoid exposing unnecessary secrets or privileged browser sessions.

Risk: Screenshots, traces, videos, PDFs, downloads, and temporary browser state can contain sensitive application or user data.

Mitigation: Keep artifacts local or under controlled CI retention, review them before sharing, and avoid persistent browser state unless the repository already standardizes it.

Risk: Automating destructive, production, financial, medical, or otherwise high-stakes flows can cause unintended real-world effects.

Mitigation: Use staging or local environments for high-stakes flows and require explicit user confirmation before continuing against production.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/howerlin0329/skills/playwright-1-0-3)
- [Skill Homepage](https://clawic.com/skills/playwright)
- [Selector Strategies](artifact/selectors.md)
- [Debugging Guide](artifact/debugging.md)
- [Testing Patterns](artifact/testing.md)
- [CI Success Defaults](artifact/ci-cd.md)
- [Rendered-Page Extraction Patterns](artifact/scraping.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell, JavaScript, TypeScript, YAML, and Dockerfile code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose Playwright MCP actions, npm-based installation commands, test configuration, automation scripts, debugging steps, and extraction patterns.]

## Skill Version(s):

1.0.3 (source: artifact/SKILL.md frontmatter and artifact/_meta.json; ClawHub release version 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
