## Description:

Web scraping, SERP and search API for OpenClaw through Novada MCP. Search Google, Bing, DuckDuckGo and Yandex, scrape Amazon, YouTube and LinkedIn data, extract and crawl pages, and use proxies. Use when the user needs live web data, SERP results or a search API, or asks to set up or troubleshoot the Novada connection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[novada-proxy](https://clawhub.ai/user/novada-proxy)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and agents use Novada MCP to retrieve live web and search engine results, scrape structured data from supported platforms, extract or crawl pages, and monitor changes. Developers can also use the skill's setup guidance to connect and troubleshoot the Novada service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill connects to an external Novada MCP service and requires account authorization with a Novada API key. Security evidence is positive but incomplete because one reference could not be resolved.

Mitigation: Review Novada's privacy information and authorize only an account and API key you control; reassess if the unresolved reference matters to your use.

Risk: Scraping calls are billed to the user's Novada account, and large result sets can increase usage.

Mitigation: Start with a small result limit and check the expected cost before scaling up a request.

Risk: Creating a proxy sub-account writes account data, and fetching pages may be subject to access rights and site terms.

Mitigation: Create sub-accounts only when explicitly requested, and fetch only pages the user is entitled to access while respecting site terms.

## Reference(s):

- [Novada MCP product documentation](https://novada.com/products/novada-mcp/)
- [Novada MCP ClawHub release](https://clawhub.ai/novada-proxy/skills/novada-mcp)

## Skill Output:

**Output Type(s):** [API Calls, Structured data, Text, Shell commands, Configuration instructions]

**Output Format:** [Search results, scraped records, page extracts, and Markdown setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returned data depends on the selected tool, target site, and requested result limit.]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
