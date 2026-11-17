## Description:

Search the web using Baidu AI Search Engine (BDSE). Use for live information, documentation, or research topics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dtkien182](https://clawhub.ai/user/dtkien182)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to let an agent run live Baidu web searches for current information, documentation lookups, and research queries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are sent to Baidu's AI Search service.

Mitigation: Avoid submitting sensitive or confidential queries unless that data sharing is acceptable for the intended use.

Risk: The skill requires a Baidu API key stored for agent execution.

Mitigation: Keep the OpenClaw configuration private, do not commit the key, and rotate it if exposure is suspected.

## Reference(s):

- [Baidu API Key Setup Guide](references/apikey-fetch.md)
- [Baidu AI Search API key console](https://console.bce.baidu.com/ai-search/qianfan/ais/console/apiKey)
- [Baidu AI Search API endpoint](https://qianfan.baidubce.com/v2/ai_search/web_search)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration]

**Output Format:** [JSON search results printed to stdout, with Markdown setup guidance in the artifact references.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BAIDU_API_KEY; result count is capped at 50 and freshness can filter by preset or explicit date ranges.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
