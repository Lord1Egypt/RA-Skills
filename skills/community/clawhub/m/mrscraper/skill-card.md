## Description:

Read web pages, search the web, and run AI scrapers with natural-language instructions through the MrScraper API

This skill is ready for commercial/non-commercial use.

## Publisher:

[ai-mrscraper](https://clawhub.ai/user/ai-mrscraper)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use MrScraper to read public web pages, search for relevant pages, and extract structured data using natural-language instructions. They can also start or rerun scraper workflows and retrieve paginated results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An exposed API token could be used to make unauthorized MrScraper requests.

Mitigation: Use an expiring token, store it in a secret manager, and keep it out of logs and outputs.

Risk: Submitted URLs, searches, and extraction instructions are sent to MrScraper; remote service behavior and data retention were not tested.

Mitigation: Review MrScraper's data handling terms and avoid sending sensitive information unless the service is approved for it.

Risk: Broad crawl or bulk reruns may process more pages or URLs than intended.

Mitigation: Set crawl and bulk limits, and review manual workflows before rerunning them.

## Reference(s):

- [MrScraper ClawHub skill page](https://clawhub.ai/ai-mrscraper/skills/mrscraper)
- [MrScraper](https://mrscraper.com/)
- [MrScraper Scraper API](https://api.mrscraper.com)
- [MrScraper Platform API](https://api.app.mrscraper.com)

## Skill Output:

**Output Type(s):** [HTML, JSON, Structured data]

**Output Format:** [HTML page content and JSON API responses containing search results, extracted data, or scraper status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may be paginated; crawl and bulk runs support configurable limits.]

## Skill Version(s):

1.1.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
