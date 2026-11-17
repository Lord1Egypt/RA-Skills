## Description:

An e-commerce prompt search assistant that retrieves commercial visual structures and master prompts from the Insight E-com Oracle Library based on a user's keyword.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kinseyho](https://clawhub.ai/user/kinseyho)

### License/Terms of Use:

MIT-0

## Use Case:

External e-commerce sellers, designers, and prompt users use this skill to search a paid prompt library for product visual concepts and master prompts by keyword, with account and payment status gating.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User queries and user identifiers are sent to a hardcoded third-party endpoint.

Mitigation: Install only if the publisher and endpoint are trusted, and avoid entering confidential business ideas unless data handling terms are clear.

Risk: Access and activation depend on an external payment flow.

Mitigation: Review the payment destination and account process before use.

Risk: The manifest requests exec authority despite no clear need in the visible code.

Mitigation: Run with the least permissions available and review execution permissions before installing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kinseyho/skills/insight-ecom-oracle)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown text with JSON-like status fields and chunked prompt results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may include account/payment status, up to five prompt results, and message chunks capped around 3800 characters.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
