## Description:

Search Google Shopping for products, fetch a full product page, and page through every store selling a product as structured JSON with price, seller, rating, and price or sale filters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and shopping workflow builders use this skill to search Google Shopping, compare retailer offers, inspect product details, and retrieve seller options through Scavio's API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shopping queries and product lookups are sent to Scavio as a third-party data provider.

Mitigation: Use the skill only when third-party shopping lookup is acceptable for the user's task and avoid sending sensitive or unnecessary query details.

Risk: The Scavio API key could be exposed if placed in source control, logs, or shared transcripts.

Mitigation: Store SCAVIO_API_KEY in an environment variable or secret manager and do not embed it in committed code or public examples.

Risk: Paginating through many store results may consume paid API credits.

Mitigation: Confirm with the user before broad pagination, monitor remaining credits, and stop once enough seller data has been collected.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/scavio-ai/skills/google-shopping-api)
- [Scavio Google Shopping API Documentation](https://scavio.dev/docs/google-shopping?utm_source=agent-skills&utm_medium=skill&utm_campaign=google-shopping-api)
- [Scavio Rate Limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=google-shopping-api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON API response examples, Python code examples, and shell configuration commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces user-directed Google Shopping API request guidance and structured JSON result handling notes; API use requires SCAVIO_API_KEY.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
