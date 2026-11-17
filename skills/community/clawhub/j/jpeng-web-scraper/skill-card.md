## Description:

Web scraping skill with JavaScript rendering support that extracts data from websites using CSS selectors, XPath, regex, or AI-powered extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jpengcheng523-netizen](https://clawhub.ai/user/jpengcheng523-netizen)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to plan scraping workflows for static or JavaScript-rendered pages, extract structured website data, and crawl multiple pages with rate limiting and robots.txt awareness.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill supports network scraping and crawling, which can reach unintended or unauthorized targets if scope is too broad.

Mitigation: Limit use to authorized targets, set small page limits, respect robots.txt, and keep rate limits enabled.

Risk: The skill can write scraped data to a local output path.

Mitigation: Verify any --output path before execution and review scraped data handling requirements before writing locally.

Risk: JavaScript rendering and multi-page crawling can increase traffic volume compared with a single static page request.

Mitigation: Use conservative wait times, crawl selectors, max-page limits, user-agent settings, and request delays.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jpengcheng523-netizen/skills/jpeng-web-scraper)
- [Publisher profile](https://clawhub.ai/user/jpengcheng523-netizen)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON]

**Output Format:** [Markdown with bash command examples and JSON output examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may describe network scraping scope, selector fields, crawl limits, rendering options, rate limiting, robots.txt handling, and optional local JSON output paths.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
