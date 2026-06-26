## Description: <br>
Web scraping, crawling, and search via Firecrawl API. Converts web pages to clean markdown/JSON optimized for AI consumption. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Moochmaniac](https://clawhub.ai/user/Moochmaniac) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to scrape single web pages, crawl websites, check crawl jobs, and search the web through Firecrawl when they need clean markdown, HTML, screenshot, or JSON output for downstream analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends requested URLs, search queries, and retrieved content to Firecrawl as a third-party scraping service. <br>
Mitigation: Use it only when sharing those URLs and content with Firecrawl is acceptable; avoid private internal URLs, secrets embedded in URLs, proprietary pages, and regulated data. <br>
Risk: Crawls, searches, screenshots, and advanced options can consume Firecrawl credits. <br>
Mitigation: Start with low crawl depth, search limits, and page limits, then increase scope after confirming expected behavior and cost. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Moochmaniac/moochmaniac-firecrawl-scraper) <br>
- [Firecrawl Scrape API Endpoint](https://api.firecrawl.dev/v1/scrape) <br>
- [Firecrawl Crawl API Endpoint](https://api.firecrawl.dev/v1/crawl) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown or JSON returned from Firecrawl API operations, with shell command examples for invocation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include crawl job status, credits used, scraped metadata, truncated markdown previews, HTML, or base64 screenshot data depending on selected formats.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
