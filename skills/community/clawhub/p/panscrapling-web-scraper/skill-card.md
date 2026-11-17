## Description:

Panscrapling Web Scraper helps agents scrape web pages with Scrapling using fast HTTP, stealthy, and dynamic browser modes to extract page text, selected elements, links, images, metadata, HTML, or Markdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dashiming](https://clawhub.ai/user/dashiming)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to fetch and extract content from public web pages, including dynamically rendered pages that require browser-based scraping. It supports web data collection workflows that return page content, selected elements, links, images, metadata, HTML, or Markdown.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup can make persistent system changes and run mutable remote installers.

Mitigation: Review before installing, run only in a sandbox or disposable environment, and require manual confirmation for Homebrew, Python, pip, Playwright, and Patchright installation steps.

Risk: Web scraping can unintentionally access internal, localhost, private-network, or cloud metadata URLs.

Mitigation: Restrict allowed targets to intended public URLs and avoid scraping internal hosts, localhost, private network ranges, and cloud metadata endpoints.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dashiming/skills/panscrapling-web-scraper)
- [Scrapling](https://github.com/D4Vinci/Scrapling)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and scraped text, HTML, JSON, or Markdown results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can return selected page content, links, images, metadata, and setup guidance.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
