## Description: <br>
Searches the web through the Baidu Qianfan V2 AI Search API and returns Chinese web search results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hanshojin](https://clawhub.ai/user/hanshojin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to query current Chinese web information through Baidu, including news, weather, stock-related searches, site-limited searches, and recency-filtered results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a sensitive Baidu Qianfan V2 API key. <br>
Mitigation: Use a key scoped to the intended use case, provide it through BAIDU_API_KEY, and avoid committing secrets to files or logs. <br>
Risk: Search queries and included user text are sent to Baidu. <br>
Mitigation: Avoid submitting confidential, regulated, or unnecessary personal data in search queries. <br>
Risk: The proxy service can expose search functionality beyond the local machine if bound to a network interface. <br>
Mitigation: Keep the service bound to localhost unless external network access is deliberate and protected. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/hanshojin/hanshojin-baidu-v2) <br>
- [Baidu Qianfan V2 application console](https://console.bce.baidu.com/qianfan/v2/ais/console/applicationConsole/application) <br>
- [Baidu Qianfan AI Search V2 endpoint](https://qianfan.baidubce.com/v2/ai_search/web_search) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires uv and BAIDU_API_KEY; search requests accept a query, top_k from 1 to 20, optional recency filtering, and optional site filtering.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
