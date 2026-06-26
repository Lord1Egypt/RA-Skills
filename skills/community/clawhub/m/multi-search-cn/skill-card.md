## Description: <br>
Aggregates Chinese web search by fetching parseable DuckDuckGo HTML results with the cn-zh locale and generating direct links for Bing China, Baidu, Sogou, and 360 Search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ScottLiu007](https://clawhub.ai/user/ScottLiu007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and agents use this skill when they need Chinese web search assistance, domestic search-engine deep links, or an API-key-free fallback when Brave or Google search is unavailable. It returns DuckDuckGo parsed results when available and direct search URLs for manual browser follow-up. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Default searches send query terms to DuckDuckGo. <br>
Mitigation: Avoid confidential or sensitive search terms in default mode; use --urls-only when local link generation is sufficient. <br>
Risk: Search-engine HTML parsing can fail because of rate limits, network controls, page changes, JavaScript, or captcha protections. <br>
Mitigation: Report failures clearly and provide direct engine links for browser-based follow-up instead of claiming full search-engine crawling. <br>
Risk: High-frequency automated use may violate search-engine expectations or terms. <br>
Mitigation: Keep request rates low and review applicable search-engine robots and service terms before automation. <br>


## Reference(s): <br>
- [Multi-Search-CN reference](reference.md) <br>
- [ClawHub release page](https://clawhub.ai/ScottLiu007/multi-search-cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown-style search results and direct search links, with optional JSON output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default mode sends the query to DuckDuckGo HTML; --urls-only generates search-engine links without making a network request.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
