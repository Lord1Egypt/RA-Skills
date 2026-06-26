## Description: <br>
Browser automation via Playwright MCP for navigating websites, clicking elements, filling forms, taking screenshots, extracting data, and debugging real browser workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[howerlin0329](https://clawhub.ai/user/howerlin0329) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to choose and execute Playwright MCP actions, direct Playwright scripts, browser tests, rendered-page extraction, screenshots, downloads, and debugging workflows when static fetch is insufficient. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browser automation can send requests, form input, cookies, uploads, and page interactions to user-directed websites. <br>
Mitigation: Use scoped test accounts, prefer staging or local environments for sensitive flows, and confirm high-stakes production actions before running them. <br>
Risk: Screenshots, traces, videos, PDFs, downloads, and saved authentication state can contain sensitive data. <br>
Mitigation: Keep browser state temporary by default and review generated artifacts before sharing, committing, or storing them. <br>
Risk: Optional Playwright tooling installation depends on npm packages. <br>
Mitigation: Install only in environments where npm-based Playwright tooling is trusted and acceptable. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/howerlin0329/playwright-1-0-3) <br>
- [Skill homepage](https://clawic.com/skills/playwright) <br>
- [Selector Strategies](selectors.md) <br>
- [Debugging Guide](debugging.md) <br>
- [Testing Patterns](testing.md) <br>
- [CI Success Defaults](ci-cd.md) <br>
- [Rendered-Page Extraction Patterns](scraping.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration, markdown] <br>
**Output Format:** [Markdown guidance with inline shell, JavaScript, TypeScript, YAML, and Dockerfile examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide browser actions that create local screenshots, traces, videos, PDFs, downloads, temporary browser state, or Playwright reports.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence); artifact frontmatter version 1.0.3 <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
