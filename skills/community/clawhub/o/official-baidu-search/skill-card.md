## Description: <br>
Searches the web through the Baidu AI Search API to retrieve real-time information and search results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[erxiza](https://clawhub.ai/user/erxiza) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to query Chinese web content through a local FastAPI proxy backed by Baidu AI Search. It supports real-time, recency-filtered, and site-filtered search workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to Baidu using the configured API key and may include sensitive user-provided text. <br>
Mitigation: Use a dedicated Baidu API key with quota limits and avoid sending personal, confidential, or secret information in search queries. <br>
Risk: Exposing the local FastAPI service beyond the host could allow unintended use of the configured Baidu API key. <br>
Mitigation: Run the service on 127.0.0.1 unless it is intentionally secured for network access. <br>
Risk: The service depends on a private environment variable for authentication. <br>
Mitigation: Keep the .env file private and do not commit or share the BAIDU_API_KEY. <br>


## Reference(s): <br>
- [Official Baidu Search on ClawHub](https://clawhub.ai/erxiza/official-baidu-search) <br>
- [Baidu Qianfan AI Search application console](https://console.bce.baidu.com/qianfan/ais/console/applicationConsole/application) <br>
- [Baidu AI Search web search API endpoint](https://qianfan.baidubce.com/v2/ai_search/web_search) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Shell commands, Configuration] <br>
**Output Format:** [JSON search responses with markdown setup and curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search requests require BAIDU_API_KEY and accept query, top_k, recency_filter, and site_filter parameters.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
