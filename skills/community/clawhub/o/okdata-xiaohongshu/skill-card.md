## Description:

Retrieves public Xiaohongshu (RedNote) data through Okdata, including notes, accounts, trends, creators, shop products, reviews, images, topics, keywords, and videos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[conn-ho](https://clawhub.ai/user/conn-ho)

### License/Terms of Use:

MIT-0

## Use Case:

People and agents that need public Xiaohongshu data can search notes, accounts, trends, creators, products, reviews, and related content through Okdata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using the documented API can send query parameters to api.okdata.online, and some calls require an API key; paid requests incur per-call charges.

Mitigation: Review query contents and endpoint pricing before calls, and keep the API key in secret configuration rather than displaying or placing it in a URL.

## Reference(s):

- [Xiaohongshu API documentation](https://okdata.online/apis/xiaohongshu/?src=skill-okdata-xiaohongshu)
- [Okdata agent setup guide](https://okdata.online/agents.md)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Text data responses over MCP or JSON responses over HTTP]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may be paginated; documented calls cost $0.02–$0.04 each.]

## Skill Version(s):

0.2.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
