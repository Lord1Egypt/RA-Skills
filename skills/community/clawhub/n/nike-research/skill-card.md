## Description:

Researches Nike products, categories, reviews, colorways, and nearby stores through the Crawlora API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Shoppers and shopping assistants use this skill to browse Nike products, compare prices and colorways, review customer feedback, and find nearby stores.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Product queries and nearby-store coordinates are sent to Crawlora, a third-party service.

Mitigation: Avoid sending sensitive searches or precise coordinates unless needed, and confirm users are comfortable using the service.

Risk: The Crawlora API key could be exposed if embedded in prompts, commands, or shared logs.

Mitigation: Keep CRAWLORA_API_KEY in the environment and redact it from shared output and logs.

Risk: Keyword searches may return recommended products instead of a true match.

Mitigation: Check product names and details before presenting a result as a match.

## Reference(s):

- [Nike research endpoint reference](reference/endpoints.md)
- [ClawHub release page](https://clawhub.ai/crawlora-org/skills/nike-research)
- [Crawlora API service](https://crawlora.net)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Markdown summaries or structured JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search and review results are paginated; product details and nearby-store listings depend on the requested item or location.]

## Skill Version(s):

1.0.16 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
