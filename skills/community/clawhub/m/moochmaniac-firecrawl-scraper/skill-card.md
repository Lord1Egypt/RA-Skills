## Description:

Web scraping, crawling, and search via the Firecrawl API, converting web pages into markdown, HTML, screenshots, or JSON for agent workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moochmaniac](https://clawhub.ai/user/moochmaniac)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to scrape individual pages, crawl sites, search the web, and turn web content into cleaner markdown or structured JSON for analysis, RAG, summarization, and research workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: URLs, search terms, crawl scopes, and the Firecrawl API key are sent to Firecrawl.

Mitigation: Avoid private intranet URLs, confidential documents, sensitive search terms, or targets the user is not authorized to scrape.

Risk: Crawls, searches, screenshots, and advanced features can consume Firecrawl credits.

Mitigation: Start with low depth and limit values, and monitor credit usage before larger crawls.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/moochmaniac/skills/moochmaniac-firecrawl-scraper)
- [Publisher Profile](https://clawhub.ai/user/moochmaniac)
- [Firecrawl API Endpoint](https://api.firecrawl.dev/v1/scrape)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown or JSON returned through command-line output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include crawl job identifiers, status details, credit usage, scraped content previews, or raw Firecrawl API responses.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
