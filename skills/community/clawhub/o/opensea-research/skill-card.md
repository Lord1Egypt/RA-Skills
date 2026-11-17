## Description:

Researches OpenSea NFT collections, items, marketplace activity, listings, offers, traits, categories, chains, and creator profiles via the Crawlora API, returning clean JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agents use this skill to inspect public OpenSea marketplace data, compare collection activity, and retrieve normalized NFT collection, item, trait, listing, offer, sale, chain, category, and creator profile data through Crawlora.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries are sent to Crawlora with the configured API key, including collection, wallet or profile identifiers, and query filters.

Mitigation: Use a dedicated Crawlora API key and avoid submitting requests you do not want associated with that API account.

Risk: The helper performs live HTTP GET requests to an external API service.

Mitigation: Review the documented route catalog before use and run the helper only in an environment where outbound requests to Crawlora are acceptable.

## Reference(s):

- [Endpoint Reference](reference/endpoints.md)
- [Crawlora API Base](https://api.crawlora.net/api/v1)
- [Crawlora](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills)
- [ClawHub Skill Page](https://clawhub.ai/crawlora-org/skills/opensea-research)

## Skill Output:

**Output Type(s):** [JSON, shell commands, configuration, guidance]

**Output Format:** [JSON API responses with Markdown guidance and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses CRAWLORA_API_KEY and GET requests to documented Crawlora OpenSea routes.]

## Skill Version(s):

1.0.10 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
