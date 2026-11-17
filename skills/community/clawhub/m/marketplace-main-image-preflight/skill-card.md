## Description:

Reviews an existing product main image against a named marketplace, region, and category, then prepares a traceable preflight card and one seller-approved cleanup edit.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce sellers use this skill to prepare one existing product image for a specific marketplace listing, region, and category. It produces a requirement-aware preflight card and can make one focused cleanup edit after seller approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The shared Beatra authorization grants broader account access than image preflight requires, including unrelated media and voice capabilities.

Mitigation: Prefer an image-only authorization option when available; explain that revoking the shared authorization may disconnect other Beatra skills.

Risk: A selected image is uploaded to an external service for processing.

Mitigation: Upload only images the seller is comfortable having processed externally.

Risk: Image edits can incur charges and may change product details or listing suitability.

Mitigation: Require explicit seller approval for each paid edit and have the seller compare the result with current marketplace guidance before upload.

Risk: Installation analytics are automatically reported.

Mitigation: Disclose this behavior to the user before installation or use.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/beatra-ai/skills/marketplace-main-image-preflight)
- [Main image preflight workflow](references/workflow.md)
- [Installation and authorization](references/installation-and-auth.md)
- [Updates and security](references/updates-and-security.md)
- [Beatra MCP service](https://mcp.beatra.ai/mcp)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Image files]

**Output Format:** [Markdown preflight card and, when approved, one edited image file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One existing image, one listing target, and at most one seller-approved edit; the marketplace makes the final listing decision.]

## Skill Version(s):

0.2.2 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
