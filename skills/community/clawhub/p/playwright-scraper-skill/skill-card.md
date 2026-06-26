## Description: <br>
Playwright-based web scraping OpenClaw Skill with anti-bot protection. Successfully tested on complex sites like Discuss.com.hk. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[waisimon](https://clawhub.ai/user/waisimon) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to fetch browser-rendered web content with Playwright, choosing a simple scraper for regular dynamic pages or a stealth scraper for sites that require more browser realism. It supports configurable wait time, headless mode, user agent, screenshots, and optional saved HTML. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Stealth scraping may be used to bypass anti-bot controls or access restrictions without authorization. <br>
Mitigation: Use the skill only on sites you own or are explicitly permitted to automate, and do not use stealth mode to bypass Cloudflare challenges, CAPTCHAs, rate limits, login barriers, or access controls without permission. <br>
Risk: Scraped JSON, screenshots, saved HTML, cookies, and session-derived data may contain sensitive or private information. <br>
Mitigation: Store outputs securely, limit retention, avoid committing generated artifacts, and delete screenshots, HTML, and session-related data when no longer needed. <br>
Risk: Browser automation depends on Playwright and local Chromium behavior, which may change or expose environment-specific sandbox risk. <br>
Mitigation: Pin and update Playwright, install browsers from trusted sources, and keep browser sandboxing enabled where the runtime environment allows. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/waisimon/playwright-scraper-skill) <br>
- [Playwright documentation](https://playwright.dev/) <br>
- [puppeteer-extra stealth plugin reference](https://github.com/berstend/puppeteer-extra/tree/master/packages/puppeteer-extra-plugin-stealth) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code, text, files] <br>
**Output Format:** [Markdown guidance with bash examples; scraper scripts emit JSON text and can write screenshot or HTML files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The simple scraper returns page title, URL, text preview, metadata, and elapsed time; the stealth scraper can also report Cloudflare detection, screenshot path, saved HTML path, and extracted links.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter, package.json, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
