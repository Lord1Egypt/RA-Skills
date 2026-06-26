## Description: <br>
Provides an OpenClaw search helper for users in mainland China that falls back across Volcengine, Tavily, SearchAPI, and a local multi-search engine integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gki38511](https://clawhub.ai/user/gki38511) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users in mainland China use this skill to configure and invoke web search through multiple API providers with automatic fallback when a provider is unavailable. <br>

### Deployment Geography for Use: <br>
China (mainland) <br>

## Known Risks and Mitigations: <br>
Risk: The security review flags unsafe third-party GitHub login advice. <br>
Mitigation: Use official GitHub login only and do not enter GitHub credentials on githubs.cn or any unofficial GitHub mirror. <br>
Risk: Search queries and API credentials may be sent to external search providers. <br>
Mitigation: Use revocable, low-privilege API keys, avoid sensitive searches, and review each configured provider before deployment. <br>
Risk: The security review says the Volcengine/open.feedcoopapi.com path is under-disclosed. <br>
Mitigation: Review or disable the Volcengine/open.feedcoopapi.com provider path unless its endpoint and data handling are approved. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/gki38511/openclaw-china-search-tips) <br>
- [Tavily](https://app.tavily.com/home) <br>
- [SearchAPI](https://www.searchapi.io/) <br>
- [Volcengine search API endpoint](https://open.feedcoopapi.com/search_api/web_search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command snippets; runtime helper output is a dictionary containing success status, source, results, and answer fields.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires one or more search API keys through environment variables and sends configured queries to external search providers.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
