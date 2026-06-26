## Description: <br>
Playwright-based web scraping OpenClaw Skill with anti-bot protection. Successfully tested on complex sites like Discuss.com.hk. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[itsjustFred](https://clawhub.ai/user/itsjustFred) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and automation users use this skill to choose and run Playwright-based scraping flows for regular, JavaScript-rendered, or anti-bot protected websites when they are authorized to automate the target site. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is designed for scraping sites with anti-bot protections. <br>
Mitigation: Use it only where automation is authorized and permitted by the target site's rules. <br>
Risk: Captured page content, screenshots, or HTML can be saved to local paths. <br>
Mitigation: Run the skill in an isolated environment, avoid sensitive or logged-in pages, restrict output paths to a safe directory, and delete captured artifacts when no longer needed. <br>
Risk: Browser automation depends on Playwright and Chromium behavior that can change over time. <br>
Mitigation: Keep Playwright and Chromium updated and review scraper results before relying on them. <br>


## Reference(s): <br>
- [Playwright Official Docs](https://playwright.dev/) <br>
- [puppeteer-extra-plugin-stealth](https://github.com/berstend/puppeteer-extra/tree/master/packages/puppeteer-extra-plugin-stealth) <br>
- [ClawHub Skill Page](https://clawhub.ai/itsjustFred/playwright-scraper-skill-1-2-0) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code, JSON, Files] <br>
**Output Format:** [Markdown guidance with bash examples; scraper scripts emit JSON and can save screenshots or HTML files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Output may include captured page text, metadata, screenshot paths, and optional saved HTML depending on environment variables.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter, package.json, CHANGELOG, released 2026-02-07) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
