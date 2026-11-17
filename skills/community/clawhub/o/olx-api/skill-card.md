## Description:

Searches seven OLX marketplaces and retrieves classified listings, seller details, category and location data as structured JSON through Scavio.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to search OLX listings, inspect ads and seller details, and build localized market research or monitoring workflows.

### Deployment Geography for Use:

Poland, Romania, Portugal, Bulgaria, Ukraine, Kazakhstan, and Uzbekistan

## Known Risks and Mitigations:

Risk: Requests use an API key with an external service; the security review rates the skill benign with medium confidence.

Mitigation: Keep SCAVIO_API_KEY in an environment variable or secret store, and review requests before execution.

Risk: The security analysis had partial coverage because several local references were unresolved.

Mitigation: Review the complete skill and any unresolved references before installation.

## Reference(s):

- [OLX API documentation](https://scavio.dev/docs/olx-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=olx-api)
- [Scavio OLX API overview](https://scavio.dev/olx-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=olx-api)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [Structured listing data with concise natural-language summaries when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Live classified listings and seller or category details; prices use each marketplace's currency.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata; skill frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
