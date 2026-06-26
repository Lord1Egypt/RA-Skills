## Description: <br>
Playwright-based web scraping OpenClaw Skill with anti-bot protection. Successfully tested on complex sites like Discuss.com.hk. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[onlyloveher](https://clawhub.ai/user/onlyloveher) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to scrape JavaScript-rendered websites with Playwright, including sites that apply common anti-bot checks. It can return page text, metadata, selected links, screenshots, and optional saved HTML for authorized scraping workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact includes Xianyu/Goofish login automation with a hardcoded phone number and SMS-code triggering behavior. <br>
Mitigation: Remove or ignore the Xianyu scripts unless the account workflow is explicitly authorized, and delete the hardcoded phone number before use. <br>
Risk: Scraping runs can save screenshots or HTML that may contain sensitive page content. <br>
Mitigation: Store outputs only in approved locations, review them as potentially sensitive data, and delete them when they are no longer needed. <br>
Risk: The skill is intended for web scraping and anti-bot scenarios that may violate site rules if used without permission. <br>
Mitigation: Use the skill only on sites where the operator is authorized to scrape and where the workflow complies with applicable terms and laws. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/onlyloveher/playwright-scraper-cn) <br>
- [Publisher profile](https://clawhub.ai/user/onlyloveher) <br>
- [Playwright documentation](https://playwright.dev/) <br>
- [puppeteer-extra-plugin-stealth](https://github.com/berstend/puppeteer-extra/tree/master/packages/puppeteer-extra-plugin-stealth) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, files, guidance] <br>
**Output Format:** [JSON emitted to stdout, with optional screenshot and HTML files; documentation includes Markdown and shell command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runtime behavior is controlled by command-line URL input and environment variables such as WAIT_TIME, HEADLESS, SCREENSHOT_PATH, SAVE_HTML, and USER_AGENT.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter, package.json, CHANGELOG, server release) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
