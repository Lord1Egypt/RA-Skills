## Description:

Search Poshmark US and Canada for sold and active listings, and inspect listings, seller closets, categories, brands, and Posh Parties.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and resellers use the skill to research Poshmark sold prices, compare them with active listings, and inspect listings or seller closets.

### Deployment Geography for Use:

United States and Canada

## Known Risks and Mitigations:

Risk: Requests use an API key with api.scavio.dev, and scanner coverage was partial.

Mitigation: Review the documented service requests and unresolved references, and only configure an API key if you are comfortable sending it to that service.

## Reference(s):

- [Poshmark sold prices API documentation](https://scavio.dev/docs/poshmark-sold?utm_source=agent-skills&utm_medium=skill&utm_campaign=poshmark-api)
- [Scavio Poshmark API overview](https://scavio.dev/poshmark-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=poshmark-api)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [Structured JSON results with concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [15 read-only endpoints; each call costs one credit. Sold search is capped at 480 listings per query and filter combination.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
