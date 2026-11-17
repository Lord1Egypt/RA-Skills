## Description:

Searches the web through the Baidu AI Search API to retrieve timely Chinese web results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[erxiza](https://clawhub.ai/user/erxiza)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query current Chinese web content, including news, weather, stock information, and site-specific results, through a local Baidu API-backed search service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local Baidu API proxy may be exposed to unauthenticated network callers if started on a non-local interface.

Mitigation: Run the service bound to 127.0.0.1 or place it behind trusted authentication before allowing network access.

Risk: The skill requires a BAIDU_API_KEY and sends search queries to Baidu.

Mitigation: Protect the API key and .env file, monitor quota and cost, and avoid sensitive searches unless that data handling is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/erxiza/skills/official-baidu-search)
- [Baidu Intelligent Cloud application console](https://console.bce.baidu.com/qianfan/ais/console/applicationConsole/application)
- [Baidu AI Search API endpoint](https://qianfan.baidubce.com/v2/ai_search/web_search)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON search results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results include title, URL, snippet, site name, and total result count.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
