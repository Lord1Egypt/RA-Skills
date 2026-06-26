## Description: <br>
Scrape and compare product prices across e-commerce sites, including Amazon, eBay, Walmart, and generic product pages, with structured JSON or CSV output for normalized pricing data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to collect public product pricing from retail pages, normalize prices, and compare results across retailers for tracking, comparison, or market-monitoring workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scraping retail pages can create privacy, terms-of-service, and site compliance issues, especially for private, logged-in, or high-volume targets. <br>
Mitigation: Use only public product pages, avoid sensitive internal or logged-in URLs, check site rules, respect robots.txt and rate limits, and keep request volumes modest. <br>
Risk: Pricing extraction may be incomplete or misleading because selectors can break, pages can be dynamically rendered, and the artifact's helper script primarily normalizes supplied results. <br>
Mitigation: Validate selectors against live page snapshots before relying on results, review extracted prices for accuracy, and treat comparisons as decision support rather than authoritative pricing records. <br>


## Reference(s): <br>
- [Site-Specific Selectors](references/selectors.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Files] <br>
**Output Format:** [Markdown guidance with shell commands plus JSON or CSV pricing output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The helper script accepts a product query or URL, reads scraped result rows from stdin, and can write JSON or CSV output to stdout or a file.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
