## Description: <br>
Browser automation guidance via Playwright MCP for navigating sites, clicking elements, filling forms, taking screenshots, extracting data, debugging workflows, and authoring tests or scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill for real-browser workflows that require rendered page state, user interaction, screenshots, downloads, Playwright tests, MCP-driven browser control, or structured extraction when static HTTP is insufficient. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browser automation can send form inputs, cookies, uploads, and page interactions to user-requested web origins. <br>
Mitigation: Use the skill only on sites and apps the user is authorized to test, and prefer local or staging environments for sensitive workflows. <br>
Risk: Screenshots, videos, PDFs, traces, reports, and temporary browser state may capture credentials or private page data. <br>
Mitigation: Restrict access and retention for generated artifacts, and avoid persistent browser sessions unless the repository already standardizes that workflow or the user explicitly requests it. <br>
Risk: Optional installation of Playwright tooling downloads package metadata and tarballs from npm. <br>
Mitigation: Install only when the user trusts npm package retrieval and the local environment is allowed to fetch Playwright or Playwright MCP dependencies. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/playwright) <br>
- [Skill Homepage](https://clawic.com/skills/playwright) <br>
- [Playwright npm Package](https://registry.npmjs.org/playwright) <br>
- [Playwright MCP npm Package](https://registry.npmjs.org/@playwright/mcp) <br>
- [Selector Strategy and Frame Handling](artifact/selectors.md) <br>
- [Debugging Guide](artifact/debugging.md) <br>
- [Testing Patterns](artifact/testing.md) <br>
- [CI Success Defaults](artifact/ci-cd.md) <br>
- [Rendered-Page Extraction Patterns](artifact/scraping.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash, JavaScript, TypeScript, YAML, and Dockerfile examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May recommend browser actions, test commands, Playwright configuration, CI snippets, screenshots, PDFs, traces, reports, or extraction scripts depending on the user task.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
