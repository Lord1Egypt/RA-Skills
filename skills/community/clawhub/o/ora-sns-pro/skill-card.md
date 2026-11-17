## Description:

Searches LinkedIn, Facebook, Twitter/X, and Instagram profiles by keyword or by company/domain reverse lookup for trade and business lead discovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oraagent](https://clawhub.ai/user/oraagent)

### License/Terms of Use:

MIT-0

## Use Case:

External users, sales teams, and business development agents use this skill to discover social media homepages for companies, prospects, partners, or competitors from keywords, company names, or domains.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads a local AuthToken and logs part of the token during API calls.

Mitigation: Use a token created only for this provider, restrict access to OraAgent.key, and remove token-prefix logging before deployment.

Risk: Business search terms, domains, company names, and lead lists are sent to an external provider API.

Mitigation: Avoid confidential lead lists or regulated customer data unless an appropriate privacy notice and data-handling review are in place.

Risk: Responses can include provider-supplied payment or renewal links.

Mitigation: Validate configured payment URLs and make clear to users that upgrade links are provider-supplied commercial links.

Risk: API-returned text is formatted into Markdown results.

Mitigation: Escape or validate returned fields before display so external content cannot create misleading Markdown.

## Reference(s):

- [Ora社媒主页搜索专家 on ClawHub](https://clawhub.ai/oraagent/skills/ora-sns-pro)
- [OraAgent publisher profile](https://clawhub.ai/user/oraagent)

## Skill Output:

**Output Type(s):** [Markdown, API Calls, Guidance]

**Output Format:** [Markdown search results with social profile links, company metadata, and usage status text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results are limited by the provider API; keyword searches return up to 20 records and company/domain reverse lookups return up to 5 records.]

## Skill Version(s):

1.0.7 (source: server release evidence; artifact manifest reports 3.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
