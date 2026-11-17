## Description:

Linkfox 1688货源 is a one-stop 1688 sourcing toolkit for product search, bestseller discovery, image-based sourcing, and authorized procurement workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to find and compare 1688 suppliers and products, run image-based same-product sourcing, and complete authorized procurement tasks such as order preview, order creation, payment link retrieval, status checks, logistics tracking, cancellation, and receipt confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses account-scoped LinkFox API access for 1688 sourcing and procurement.

Mitigation: Install only when the publisher is trusted, keep API keys sensitive, and avoid exposing generated keys or shell profile exports.

Risk: Procurement actions such as creating orders, obtaining payment links, cancelling orders, or confirming receipt can affect real transactions.

Mitigation: Require explicit user confirmation and review key details such as item, order ID, amount, and status before each action.

Risk: Custom LINKFOX_* endpoint variables could redirect requests away from the intended service.

Mitigation: Use default endpoints unless a custom endpoint has been deliberately reviewed and trusted.

Risk: Local images uploaded for image search may become accessible through generated URLs.

Mitigation: Upload only images that are safe to share through a temporary URL.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-1688-sourcing)
- [1688 procurement reference](references/linkfox-1688-procurement.md)
- [1688 image search reference](references/linkfox-1688-search-by-image.md)
- [DLD product billboard reference](references/linkfox-dld-product-billboard.md)
- [DLD product search reference](references/linkfox-dld-product-search.md)
- [Onboarding reference](references/onboarding.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with inline shell commands and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tool runs can return JSON summaries and may save detailed response files for later inspection.]

## Skill Version(s):

1.2.3 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
