## Description:

Looks up Macy's product details and customer reviews by product ID and retrieves search-box suggestions through Crawlora.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Users and agents with a Macy's product ID can check its price, variants, and customer reviews or explore autocomplete suggestions before making recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Product lookup and suggestion queries are sent to Crawlora, a third-party service.

Mitigation: Avoid personal or secret information in queries and use the service only if its data handling is acceptable.

Risk: Exposure of the Crawlora API key could allow unauthorized use.

Mitigation: Keep CRAWLORA_API_KEY private; never put it in query strings or committed files.

## Reference(s):

- [Macy's Research on ClawHub](https://clawhub.ai/crawlora-org/skills/macys-research)
- [Macy's API endpoint reference](reference/endpoints.md)
- [Crawlora](https://crawlora.net)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON data]

**Output Format:** [Text guidance and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Product lookups require a known numeric product ID; suggestions do not return products.]

## Skill Version(s):

1.0.16 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
