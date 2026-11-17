## Description:

Search for products on Naver Shopping. Use when the user wants to find product prices, links, or compare items in the Korean market.

This skill is ready for commercial/non-commercial use.

## Publisher:

[twbeatles](https://clawhub.ai/user/twbeatles)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to search Naver Shopping for Korean-market product listings, prices, and links, including comparing items by relevance, date, or price sort order.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Naver API credentials may be stored in environment variables or local credential files.

Mitigation: Install only where Naver Shopping API access is intended, restrict local credential file access, and avoid sharing credential-bearing environments.

Risk: Product search queries are sent to Naver to retrieve shopping results.

Mitigation: Avoid submitting confidential or sensitive search terms unless sharing them with Naver is acceptable.

## Reference(s):

- [Naver Shopping Open API endpoint](https://openapi.naver.com/v1/search/shop.json)

## Skill Output:

**Output Type(s):** [JSON, shell commands, configuration guidance]

**Output Format:** [JSON search results or JSON error messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Naver API credentials; display is clamped to 1-100 and sort is one of sim, date, asc, or dsc.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
