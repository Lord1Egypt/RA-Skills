## Description:

Playwright-based web scraping OpenClaw Skill with anti-bot protection. Successfully tested on complex sites like Discuss.com.hk.

This skill is ready for commercial/non-commercial use.

## Publisher:

[waisimon](https://clawhub.ai/user/waisimon)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to scrape JavaScript-rendered websites with Playwright, choosing a simple scraper for ordinary dynamic pages or a stealth-oriented scraper for sites with anti-bot checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stealth scraping weakens normal browser automation signals and can be used against sites where access is not authorized.

Mitigation: Use the skill only for sites you are authorized to access, and review target terms and internal policy before running stealth mode.

Risk: The scripts can save screenshots and HTML that may contain sensitive or authenticated page content.

Mitigation: Avoid authenticated or sensitive pages, write outputs to a dedicated directory, and delete or protect captured files after review.

Risk: The skill launches a browser and fetches arbitrary URLs from command-line input.

Mitigation: Run it in an isolated environment with constrained network and filesystem access.

Risk: The documentation describes an optional deep-scraper install path that is outside this release evidence.

Mitigation: Do not install or use that optional dependency unless it is separately reviewed and pinned.

## Reference(s):

- [Playwright Official Docs](https://playwright.dev/)
- [puppeteer-extra-plugin-stealth](https://github.com/berstend/puppeteer-extra/tree/master/packages/puppeteer-extra-plugin-stealth)
- [Playwright Scraper Skill on ClawHub](https://clawhub.ai/waisimon/skills/playwright-scraper-skill)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell commands; scraper scripts emit JSON and may save screenshot or HTML files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scraper output includes page title, URL, content preview, elapsed time, and optional screenshot or HTML file paths.]

## Skill Version(s):

1.2.0 (source: frontmatter, package.json, CHANGELOG, ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
