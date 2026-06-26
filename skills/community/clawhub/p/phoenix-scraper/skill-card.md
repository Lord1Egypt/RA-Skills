## Description: <br>
Phoenix Scraper helps agents retrieve web content through a three-tier failover chain using Brave Search API, Bright Data Web Unlocker, and Playwright for JavaScript-rendered or bot-protected pages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stevojarvisai-star](https://clawhub.ai/user/stevojarvisai-star) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to scrape public web pages that may require search-index fallback, proxy unlocking, JavaScript rendering, or browser automation. It is suited for job-board pages, news sites, social monitoring workflows that use X API v2, and other public pages where standard HTTP fetching may fail. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Target URLs and request metadata may be sent to Brave Search, Bright Data, and X API endpoints. <br>
Mitigation: Use only approved public URLs, avoid internal or token-bearing URLs, and confirm authorization before sending sensitive targets to external providers. <br>
Risk: Bright Data premium domains can increase request cost for heavily protected sites. <br>
Mitigation: Monitor Bright Data zone usage and premium-domain billing before running large scraping jobs. <br>


## Reference(s): <br>
- [X API v2 Reference](references/x-api.md) <br>
- [Phoenix Scraper ClawHub release](https://clawhub.ai/stevojarvisai-star/phoenix-scraper) <br>


## Skill Output: <br>
**Output Type(s):** [code, shell commands, configuration, guidance] <br>
**Output Format:** [Python helper returning a JSON-like result dictionary, with Markdown usage guidance and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The scraper returns success, html, method, url, and error fields; configuration uses provider API keys from environment variables.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
