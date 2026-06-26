## Description: <br>
Korean website specialized scraper with anti-bot protection (Naver, Coupang, Daum, Instagram). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mupengi-bot](https://clawhub.ai/user/mupengi-bot) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to collect structured JSON from Korean public web sources, including Naver blogs, cafes and news, Daum news, and Coupang product pages. It is suited for authorized scraping, search-result collection, article extraction, and product-data extraction workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts third-party sites using stealth browsing and has insufficient destination controls. <br>
Mitigation: Run only against authorized public URLs, verify site terms before use, avoid private or internal URLs, and apply network egress controls where possible. <br>
Risk: The browser launch configuration weakens Chromium isolation for scraping. <br>
Mitigation: Run in a disposable sandbox or isolated container without secrets, and avoid reusing browser profiles or sensitive credentials. <br>
Risk: The dependency set includes Playwright and stealth plugins that execute browser automation code. <br>
Mitigation: Pin and review dependencies before installation, use a patched Playwright release, and scan the installed package tree before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mupengi-bot/korean-scraper) <br>
- [Playwright official docs](https://playwright.dev/) <br>
- [playwright-extra-plugin-stealth](https://github.com/berstend/puppeteer-extra/tree/master/packages/puppeteer-extra-plugin-stealth) <br>
- [Naver Developers](https://developers.naver.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, JSON, Configuration] <br>
**Output Format:** [Structured JSON emitted by Node.js command-line scripts, with Markdown usage guidance and shell command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs vary by scraper target and may include titles, URLs, authors, dates, snippets, article text, product prices, ratings, review counts, image URLs, and status/error fields.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
