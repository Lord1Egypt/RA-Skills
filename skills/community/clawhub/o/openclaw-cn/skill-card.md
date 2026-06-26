## Description: <br>
通过百度 AI 搜索 API 进行网页搜索，获取实时信息和搜索结果。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yky3489](https://clawhub.ai/user/yky3489) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to query Baidu AI Search for current Chinese web results, including keyword searches, recency filters, and site-restricted searches. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms are sent to Baidu through the Baidu AI Search API. <br>
Mitigation: Avoid submitting secrets, credentials, personal data, or confidential internal information as search queries. <br>
Risk: The local FastAPI service can expose search functionality if bound beyond localhost. <br>
Mitigation: Run the service on 127.0.0.1 unless intentional network exposure is required. <br>
Risk: The skill requires a Baidu API key. <br>
Mitigation: Store BAIDU_API_KEY in the environment or a local .env file and avoid committing or sharing it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yky3489/openclaw-cn) <br>
- [Baidu AI Search API documentation](https://cloud.baidu.com/doc/WENXINWORKSHOP/s/2m0u2qdmd) <br>
- [Baidu Qianfan application console](https://console.bce.baidu.com/qianfan/ais/console/applicationConsole/application) <br>


## Skill Output: <br>
**Output Type(s):** [API calls, JSON, text] <br>
**Output Format:** [JSON search results with titles, URLs, snippets, site names, and result counts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires BAIDU_API_KEY and sends search queries to Baidu.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
