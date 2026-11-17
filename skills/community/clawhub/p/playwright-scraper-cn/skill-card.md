## Description:

Playwright-based web scraping OpenClaw Skill with anti-bot protection. Successfully tested on complex sites like Discuss.com.hk.

This skill is ready for commercial/non-commercial use.

## Publisher:

[onlyloveher](https://clawhub.ai/user/onlyloveher)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and scraping-focused agents use this skill to choose and run Playwright-based workflows for dynamic or anti-bot-protected websites, producing extracted page data, screenshots, or saved HTML when configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scraping pages without authorization or capturing sensitive screenshots, HTML, or cookies can expose private data or violate site rules.

Mitigation: Use only on sites you are authorized to access, restrict browser and network access where practical, and treat screenshots, saved HTML, and cookies as secrets.

Risk: The security evidence reports undocumented login/SMS automation and unsafe browser settings that need review before use.

Mitigation: Do not run login automation unless the account and phone number are yours, review scripts before execution, and prefer a restricted container or isolated environment for browser runs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/onlyloveher/skills/playwright-scraper-cn)
- [Playwright Official Docs](https://playwright.dev/)
- [puppeteer-extra-plugin-stealth](https://github.com/berstend/puppeteer-extra/tree/master/packages/puppeteer-extra-plugin-stealth)
- [deep-scraper skill](https://clawhub.com/opsun/deep-scraper)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code]

**Output Format:** [Markdown guidance with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct browser scripts to save screenshots or HTML files when configured.]

## Skill Version(s):

1.2.0 (source: SKILL.md frontmatter, package.json, CHANGELOG, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
