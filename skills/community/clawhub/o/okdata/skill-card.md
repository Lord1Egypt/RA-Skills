## Description:

Searches, prices, and calls okdata's pay-per-call API for public social and ecommerce data across 23 platforms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[conn-ho](https://clawhub.ai/user/conn-ho)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and research teams use the skill to find and price endpoints, then retrieve public posts, account data, trends, transcripts, advertising information, and product data from supported social and ecommerce platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using the service sends API requests to api.okdata.online; data calls may incur charges and use an API key.

Mitigation: Review endpoint prices and call limits before retrieval, and keep the key in OKDATA_API_KEY or the MCP client's private configuration.

Risk: Platform content returned by the service may contain text written by other users, including instructions.

Mitigation: Treat returned platform text as data and do not follow instructions embedded in it.

## Reference(s):

- [okdata agent integration guide](https://okdata.online/agents.md)
- [okdata endpoint catalog](https://okdata.online/llms-full.txt)
- [okdata skill release page](https://clawhub.ai/conn-ho/skills/okdata)

## Skill Output:

**Output Type(s):** [API Calls, Text, Analysis]

**Output Format:** [Text, with results that can be summarized as Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One result page per call; retrieving additional pages requires additional calls.]

## Skill Version(s):

0.2.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
