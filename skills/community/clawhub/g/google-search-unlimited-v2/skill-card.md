## Description: <br>
Google Search Unlimited V2 helps agents run cached web searches with rate limiting, provider fallbacks, and cost-aware use of OpenClaw tools and free APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gloriaolk](https://clawhub.ai/user/gloriaolk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and agents use this skill to perform web searches, reuse cached results, process batches of search queries, and reduce paid search API usage through free-first fallback behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms may be sent to external providers and stored in local cache or exported result files. <br>
Mitigation: Avoid submitting secrets or sensitive personal data, review cache/export paths before use, and purge local search data when retention is not required. <br>
Risk: Some artifact behavior and documentation reference mocked or test search results, which can make provider provenance unclear. <br>
Mitigation: Use only deployments that clearly separate live search from mock/test output, and verify each result's provider and source before relying on it. <br>
Risk: Fallback search behavior can mix providers with different terms, quotas, and result quality. <br>
Mitigation: Configure the permitted search methods, monitor rate limits and costs, and review outputs for relevance and source quality. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gloriaolk/google-search-unlimited-v2) <br>
- [Publisher profile](https://clawhub.ai/user/gloriaolk) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [JSON search results and Markdown or terminal guidance with shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include query, method, cache status, cost estimate, response time, result links, snippets, and batch metrics.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release evidence; artifact frontmatter reports 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
