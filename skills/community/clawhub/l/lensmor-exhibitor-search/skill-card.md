## Description:

Finds ICP-matching exhibitors, prospects, partners, and competitors at trade shows using the Lensmor API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weilun88313](https://clawhub.ai/user/weilun88313)

### License/Terms of Use:

MIT-0

## Use Case:

B2B sales and marketing teams use this skill to discover exhibitors that match an ideal customer profile before a trade show. It supports prospect discovery, partner sourcing, and competitive mapping from a company URL or target-audience description.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends company URLs, target-audience descriptions, event IDs, and prospecting context to Lensmor.

Mitigation: Use it only for data that may be shared with Lensmor, and review Lensmor's data-handling terms before using confidential prospecting workflows.

Risk: A Lensmor API key is required for use.

Mitigation: Store LENSMOR_API_KEY in the environment or a secrets manager, and do not include the key in prompts, outputs, or shared documents.

## Reference(s):

- [Lensmor API documentation](https://api.lensmor.com/)
- [Lensmor platform](https://platform.lensmor.com)
- [ClawHub skill listing](https://clawhub.ai/weilun88313/skills/lensmor-exhibitor-search)
- [Example walkthrough](examples/saas-vendor-at-dreamforce.md)

## Skill Output:

**Output Type(s):** [Markdown, API Calls, Shell Commands, Guidance]

**Output Format:** [Markdown tables with result summaries, ICP match notes, and contextual follow-up suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires LENSMOR_API_KEY and either company_url or target_audience; optional event_id, page, and pageSize control scoping and pagination.]

## Skill Version(s):

1.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
