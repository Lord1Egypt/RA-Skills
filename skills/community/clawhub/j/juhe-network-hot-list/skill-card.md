## Description: <br>
Queries real-time trending-topic lists across major Chinese platforms including Weibo, Douyin, Kuaishou, Zhihu, Baidu, Toutiao, and Bilibili through the Juhe network hot-list API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[juhemcp](https://clawhub.ai/user/juhemcp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to retrieve and summarize current hot-search rankings from Juhe for social listening, trend checks, and agent responses to hot-topic queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Juhe API key is sent to the configured API endpoint over plain HTTP. <br>
Mitigation: Use the skill only on trusted networks unless the endpoint is changed to verified HTTPS, and rotate the key if exposure is suspected. <br>
Risk: The skill requires a Juhe API key that may be exposed if stored in local files. <br>
Mitigation: Store the key in a protected environment variable where possible and avoid committing .env files or command history containing the key. <br>
Risk: Returned hot-list data depends on the live third-party Juhe service and quota availability. <br>
Mitigation: Handle API errors and quota exhaustion as user-visible service limitations, and retry only transient network failures. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/juhemcp/juhe-network-hot-list) <br>
- [Juhe Network Hot List API](https://www.juhe.cn/docs/api/id/739) <br>
- [Juhe](https://www.juhe.cn) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Terminal table with a JSON payload for the selected hot-list entries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and a JUHE_HOTSEARCH_KEY API key; supports limit and detail options.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
