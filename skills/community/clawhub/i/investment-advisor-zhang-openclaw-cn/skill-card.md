## Description:

Searches the Chinese web through the Baidu AI Search API and returns timely, structured search results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[acceleratel](https://clawhub.ai/user/acceleratel)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill to query current Chinese web content through Baidu AI Search, including keyword, recent-time, and site-filtered searches.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An API-key-backed search service could be exposed without authentication if bound beyond localhost.

Mitigation: Run it bound to 127.0.0.1 unless authentication, TLS, rate limits, and firewall controls are added.

Risk: Sensitive search text or upstream error bodies may appear in logs or client responses.

Mitigation: Avoid sensitive queries and review logging and error-response behavior before deployment.

Risk: Search queries are sent to Baidu using the configured API key.

Mitigation: Install only when the operator is comfortable providing a Baidu API key and sending queries to Baidu.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/acceleratel/skills/investment-advisor-zhang-openclaw-cn)
- [Baidu Qianfan application console](https://console.bce.baidu.com/qianfan/ais/console/applicationConsole/application)
- [Baidu AI Search API endpoint](https://qianfan.baidubce.com/v2/ai_search/web_search)

## Skill Output:

**Output Type(s):** [Text, JSON, API Calls, Guidance]

**Output Format:** [JSON search response with result title, URL, snippet, site name, and total count; agents may summarize results as text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BAIDU_API_KEY; search requests support query, top_k, recency_filter, and site_filter.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
