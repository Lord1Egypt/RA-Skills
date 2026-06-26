## Description: <br>
Runs Baidu web searches during a conversation and returns titles, summaries, links, dates, and request metadata. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jisuapi](https://clawhub.ai/user/jisuapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to answer requests for recent web pages, official sites, policy documents, news, and topic research through Baidu search results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms are sent to Baidu through the configured API key. <br>
Mitigation: Avoid searching secrets, confidential business information, or sensitive personal data. <br>
Risk: The configured API key may incur quota or billing usage. <br>
Mitigation: Use a dedicated key where possible and monitor usage. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jisuapi/jisu-baidu) <br>
- [Baidu Qianfan Web Search API documentation](https://cloud.baidu.com/doc/qianfan-api/s/Wmbq4z7e5) <br>
- [JisuAPI](https://www.jisuapi.com/) <br>
- [JisuEPC](https://www.jisuepc.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands] <br>
**Output Format:** [JSON printed to stdout, typically summarized by the agent in Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires BAIDU_API_KEY and returns Baidu references with title, URL, snippet, date, and request ID when available.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
