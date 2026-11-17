## Description:

Run a SaaS seller's price negotiations on HAGGIN through its API, including offer review, negotiation drafting, deal follow-up, and webhook setup with explicit seller approval for buyer-facing or commitment-making actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lmfresneda](https://clawhub.ai/user/lmfresneda)

### License/Terms of Use:

MIT-0

## Use Case:

SaaS sellers and their agents use this skill to inspect HAGGIN inboxes, interpret customer offers, draft Haggins and counteroffers, manage accepted deals, and configure seller-side webhooks. The skill is designed to prepare recommendations and API request bodies while requiring seller approval before actions that affect buyers, prices, published pages, deals, or webhook secrets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access HAGGIN seller data and use a HAGGIN API key.

Mitigation: Install it only for trusted agents, prefer a read-only key for offer review, and use a full-access key only when the seller wants confirmed write actions.

Risk: Buyer-facing actions can affect negotiations, published pages, payment links, webhook endpoints, or commercial terms.

Mitigation: Review proposed request bodies and require explicit seller approval before accepting, countering, rejecting, publishing, closing, changing webhooks, or sending buyer instructions.

## Reference(s):

- [HAGGIN API Reference](artifact/references/api.md)
- [HAGGIN API Documentation](https://hagg.in/docs/api)
- [HAGGIN OpenAPI Specification](https://hagg.in/api/v1/openapi.json)

## Skill Output:

**Output Type(s):** [Analysis, API Calls, JSON, Guidance, Configuration instructions]

**Output Format:** [Markdown guidance with JSON request bodies and HAGGIN API calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires HAGGIN_API_KEY; write actions require a full-access key and explicit seller confirmation.]

## Skill Version(s):

1.0.1 (source: artifact frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
