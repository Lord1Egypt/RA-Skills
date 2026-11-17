## Description:

ScrapingAnt (scrapingant.com). Use this skill for ANY ScrapingAnt request — searching and reading data. Whenever a task involves ScrapingAnt, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use the skill to search and read web data through ScrapingAnt, including Markdown conversion, structured extraction, and extended page scraping.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup instructions can execute unverified software and introduce broader agent changes without clear user control.

Mitigation: Review the CLI and installer before use, require confirmation for setup changes, and consider disabling automatic skill synchronization.

Risk: Scraping requests pass through OOMOL and ScrapingAnt and may consume account credits.

Mitigation: Keep requests within the user's intended scope and check credit usage before large scraping jobs.

## Reference(s):

- [ScrapingAnt](https://scrapingant.com)
- [ScrapingAnt API documentation](https://docs.scrapingant.com/api-basics)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Text]

**Output Format:** [Markdown, JSON, or text returned from a scraping action]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Available fields vary by action; extended scraping can include HTML, text, cookies, headers, XHRs, and iframes.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
