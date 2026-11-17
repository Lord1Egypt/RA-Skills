## Description:

Queries public Meta Ad Library and Google Ads Transparency Center data through okdata for advertising and competitor research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[conn-ho](https://clawhub.ai/user/conn-ho)

### License/Terms of Use:

MIT

## Use Case:

Marketing researchers and competitor analysts use this skill to search public Meta and Google ad libraries by keyword or advertiser and review ad creatives, landing pages, platforms, and run dates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms are sent to the okdata API service.

Mitigation: Use the service only when its data handling is acceptable for the query, and avoid sending sensitive search terms.

Risk: A data-source call may incur a charge even when it returns no results or an upstream error.

Mitigation: Estimate the number of calls, set a max_price, and avoid retrying not_found responses.

## Reference(s):

- [okdata Meta Ads API documentation](https://okdata.online/zh/apis/meta/)
- [okdata remote MCP endpoint](https://api.okdata.online/mcp)
- [ClawHub skill release](https://clawhub.ai/conn-ho/skills/okdata-ad-library)

## Skill Output:

**Output Type(s):** [JSON, Analysis]

**Output Format:** [Structured ad-library results with concise agent-readable summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Paid per API call; results may include ad copy, advertiser details, media, platforms, and dates.]

## Skill Version(s):

0.1.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
