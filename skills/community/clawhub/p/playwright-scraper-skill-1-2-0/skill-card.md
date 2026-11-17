## Description:

Playwright-based web scraping OpenClaw Skill with anti-bot protection. Successfully tested on complex sites like Discuss.com.hk.

This skill is ready for commercial/non-commercial use.

## Publisher:

[itsjustfred](https://clawhub.ai/user/itsjustfred)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to choose and run Playwright-based scraping approaches for regular dynamic pages and anti-bot-protected public websites. It provides command guidance and scripts that return page metadata, text previews, and optional saved screenshots or HTML.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs arbitrary URLs in a browser configured to reduce automation detection.

Mitigation: Use it only against sites you are authorized to access, prefer public non-sensitive pages, and run it in a container or low-privilege environment.

Risk: Screenshots and saved HTML can capture sensitive page content, and SCREENSHOT_PATH controls where files are written.

Mitigation: Use trusted output paths in a dedicated directory, avoid private or authenticated pages, and treat generated files as sensitive until reviewed.

Risk: The documented anti-bot behavior can conflict with site access rules or terms.

Mitigation: Review site terms and robots guidance before use, and choose the simple scraper or built-in fetch path when stealth behavior is not necessary.

## Reference(s):

- [Playwright Official Docs](https://playwright.dev/)
- [puppeteer-extra-plugin-stealth](https://github.com/berstend/puppeteer-extra/tree/master/packages/puppeteer-extra-plugin-stealth)
- [deep-scraper skill](https://clawhub.com/opsun/deep-scraper)
- [ClawHub skill page](https://clawhub.ai/itsjustfred/skills/playwright-scraper-skill-1-2-0)

## Skill Output:

**Output Type(s):** [Text, JSON, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands; scraper scripts emit JSON and can save screenshot or HTML files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on target page content, wait time, user agent, headless mode, screenshot path, and SAVE_HTML settings.]

## Skill Version(s):

1.2.0 (source: SKILL.md frontmatter, package.json, CHANGELOG; ClawHub release metadata version 1.0.0 differs)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
