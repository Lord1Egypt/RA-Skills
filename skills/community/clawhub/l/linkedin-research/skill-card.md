## Description:

Researches public LinkedIn company, product, and showcase pages and discovers public products through the Crawlora API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers and business teams use this skill to look up public LinkedIn company, product, and showcase pages by ID or discover products by keyword or category for company and competitor research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requested lookup IDs, search terms, and the API key are sent to Crawlora.

Mitigation: Send only intended public lookup inputs; keep CRAWLORA_API_KEY in the environment and never hardcode or commit it.

Risk: Successful API requests may consume Crawlora credits.

Mitigation: Confirm the intended lookup before running the helper and monitor API usage.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/crawlora-org/skills/linkedin-research)
- [LinkedIn endpoint reference](artifact/reference/endpoints.md)
- [Crawlora](https://crawlora.net)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [JSON API responses or concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Public company, product, showcase, and product-directory data only; no personal profiles or private content.]

## Skill Version(s):

1.0.21 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
