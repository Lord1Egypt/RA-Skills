## Description: <br>
Browser automation via Playwright MCP for navigating websites, interacting with forms, capturing browser evidence, extracting rendered data, and debugging real browser workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhichengsong](https://clawhub.ai/user/zhichengsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to choose and apply Playwright MCP, Playwright scripts, and Playwright tests for browser automation, UI debugging, screenshots, downloads, and rendered-page extraction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browser automation can send form input, cookies, uploads, and page interactions to user-requested websites. <br>
Mitigation: Use dedicated test or staging accounts where possible, and confirm before submissions, uploads, account changes, or other state-changing actions. <br>
Risk: Optional Playwright and Playwright MCP installation can fetch npm packages at execution time. <br>
Mitigation: Verify npm packages before running npx or install commands, and install only when browser automation tooling is needed. <br>
Risk: Playwright traces, screenshots, videos, reports, downloads, and saved auth files can contain sensitive source, session, or user data. <br>
Mitigation: Treat these artifacts as sensitive outputs, store them only as needed, and avoid privileged production sessions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhichengsong/playwright-tmp) <br>
- [Skill homepage](https://clawic.com/skills/playwright) <br>
- [Playwright npm package](https://registry.npmjs.org/playwright) <br>
- [Playwright MCP npm package](https://registry.npmjs.org/@playwright%2fmcp) <br>
- [Selector Strategies](artifact/selectors.md) <br>
- [Debugging Guide](artifact/debugging.md) <br>
- [Testing Patterns](artifact/testing.md) <br>
- [CI Success Defaults](artifact/ci-cd.md) <br>
- [Rendered-Page Extraction Patterns](artifact/scraping.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline code blocks, shell commands, configuration snippets, and Playwright examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide creation of Playwright tests, scripts, MCP browser actions, screenshots, PDFs, traces, reports, downloads, and temporary browser state.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; artifact frontmatter reports 1.0.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
