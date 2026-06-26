## Description: <br>
Searches the Chinese web through the Baidu AI Search API to retrieve real-time web information and search results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[acceleratel](https://clawhub.ai/user/acceleratel) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to answer time-sensitive Chinese-web queries, including news, weather, financial information, and site-specific searches, using Baidu AI Search results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends search queries to Baidu AI Search, which may expose confidential or sensitive query text to an external provider. <br>
Mitigation: Avoid sending confidential search queries unless Baidu's handling of that data is acceptable for the intended use case. <br>
Risk: The local API service depends on a Baidu API key stored in the environment or .env file. <br>
Mitigation: Protect the .env file, use a revocable Baidu API key, and rotate or revoke the key if exposure is suspected. <br>
Risk: Exposing the local search service beyond localhost could broaden access to the API key-backed search capability. <br>
Mitigation: Keep the service bound to localhost unless a deployment review explicitly approves a broader network binding. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/acceleratel/investment-advisor-zhang-openclaw-cn) <br>
- [Baidu Qianfan application console](https://console.bce.baidu.com/qianfan/ais/console/applicationConsole/application) <br>
- [Baidu AI Search API endpoint](https://qianfan.baidubce.com/v2/ai_search/web_search) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and structured JSON search responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search requests require a query, support top_k from 1 to 20, and may include recency_filter or site_filter.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports 1.0.1 and pyproject.toml reports 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
