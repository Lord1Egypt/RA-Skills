## Description:

Provides Media Expert product prices, promotion details, store availability, product information, reviews, and store data in Poland through Scavio's API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and shopping assistants use this skill to retrieve current Media Expert prices, promotions, product details, reviews, and store information for shoppers in Poland.

### Deployment Geography for Use:

Poland

## Known Risks and Mitigations:

Risk: Shopping searches and any location supplied for nearby-store lookup are shared with Scavio; the security evidence flags a privacy disclosure gap.

Mitigation: Explain this data sharing to users and provide a location only when they want nearby-store results.

## Reference(s):

- [Scavio Media Expert API overview](https://scavio.dev/mediaexpert-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=media-expert-api)
- [Media Expert search API documentation](https://scavio.dev/docs/mediaexpert-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=media-expert-api)
- [Media Expert store stock API documentation](https://scavio.dev/docs/mediaexpert-store-stock?utm_source=agent-skills&utm_medium=skill&utm_campaign=media-expert-api)
- [ClawHub release page](https://clawhub.ai/scavio-ai/skills/media-expert-api)

## Skill Output:

**Output Type(s):** [JSON data, Guidance]

**Output Format:** [Structured JSON API responses with setup and usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Product and review text may be in Polish; store stock is an indicator bucket, not a unit count.]

## Skill Version(s):

1.0.1 (source: server release metadata in evidence.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
