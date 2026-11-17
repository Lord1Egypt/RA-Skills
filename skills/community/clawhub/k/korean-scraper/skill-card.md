## Description:

Korean website specialized scraper with anti-bot protection for major Korean sites including Naver, Coupang, and Daum.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mupengi-bot](https://clawhub.ai/user/mupengi-bot)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to collect structured JSON from public Korean blog, cafe, product, and news pages through Playwright-based CLI scripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses anti-bot behavior and weakens browser protections while running Playwright.

Mitigation: Run it only in an isolated, unprivileged container or VM and review the behavior before installation.

Risk: The CLI scripts can load user-supplied URLs for extraction.

Mitigation: Limit outbound network access to the intended public Korean domains and avoid running it on networks with sensitive internal web services.

Risk: Scraping public web content can create terms-of-service, copyright, privacy, or account-risk concerns.

Mitigation: Review site terms, copyright, privacy, robots.txt, and account policies before collecting or reusing data.

## Reference(s):

- [ClawHub Korean Scraper release](https://clawhub.ai/mupengi-bot/skills/korean-scraper)
- [Playwright Official Docs](https://playwright.dev/)
- [playwright-extra-plugin-stealth](https://github.com/berstend/puppeteer-extra/tree/master/packages/puppeteer-extra-plugin-stealth)
- [Naver Developer Center](https://developers.naver.com/)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [Structured JSON emitted by CLI scripts with Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scraped result fields vary by target site and command.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
