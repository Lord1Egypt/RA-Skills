## Description:

查询股票和概念板块的消息面热度（熔岩）。当用户问某只股票/某个概念最近消息面热不热、被哪些机构/大V提及、要点是什么、概念里哪些股票最热时使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[dustinliang666-blip](https://clawhub.ai/user/dustinliang666-blip)

### License/Terms of Use:

MIT-0

## Use Case:

Users researching A-share stocks and concepts can check recent news mention volume, summarized themes, related concepts, and anonymous agency IDs. The skill supports news monitoring for research reference and does not provide investment recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stock names, concepts, keywords, and time ranges are sent to Lava, and API calls may incur usage charges.

Mitigation: Avoid confidential client or investment information in queries, review the disclosed pricing, and protect the API key.

## Reference(s):

- [Source repository (server-resolved provenance)](https://github.com/dustinliang666-blip/lava-mcp)
- [Lava API documentation](https://lava.ai-dolphin.com/subscribe/docs)
- [Lava OpenAPI specification](https://lava.ai-dolphin.com/subscribe/v1/openapi.json)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown]

**Output Format:** [Structured Chinese text or Markdown summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summarizes mention counts, time windows, key points, and anonymous agency IDs; excludes source text and market-direction conclusions.]

## Skill Version(s):

0.1.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
