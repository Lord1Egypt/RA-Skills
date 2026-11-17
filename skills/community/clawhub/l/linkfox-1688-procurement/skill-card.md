## Description:

Helps LinkFox users run authorized 1688 procurement workflows, including OAuth checks, SKU and address lookup, order preview, guarded order creation, payment link retrieval, order tracking, logistics, cancellation, receipt confirmation, and invoicing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External LinkFox users and procurement operators use this skill to manage authorized 1688 purchasing and fulfillment tasks from authorization through invoicing. It supports guided, user-confirmed procurement actions rather than unattended end-to-end purchasing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles LinkFox API keys and may process procurement, address, order, invoice, and payment-link data.

Mitigation: Use it only in trusted workspaces, keep credentials out of shared logs and shell history, prefer secret-store or temporary credential handling, and use --no-save for sensitive responses.

Risk: Several actions can create orders, retrieve payment links, cancel orders, confirm receipt, or apply for invoices.

Mitigation: Require a separate Chinese natural-language confirmation for each high-risk action and review order, payment, cancellation, receipt, or invoice details before calling the script.

Risk: Custom LinkFox service URL environment variables can redirect calls away from the default LinkFox endpoints.

Mitigation: Avoid setting custom LinkFox service URL environment variables unless the deployment owner has explicitly approved the endpoint.

Risk: Feedback may be sent automatically and responses may be saved locally depending on size or flags.

Mitigation: Do not include API keys, tokens, full addresses, phone numbers, or payment URLs in feedback, and disable response saving for sensitive sessions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-1688-procurement)
- [1688 procurement API reference](references/api.md)
- [1688 procurement workflow map](references/workflow.md)
- [Authentication and billing onboarding](references/onboarding.md)
- [LinkFox Skills](https://skill.linkfox.com/)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, text, markdown]

**Output Format:** [Markdown guidance with inline shell commands and JSON request or response summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Small sanitized JSON responses are printed inline; larger responses may be saved as redacted JSON files unless disabled with --no-save.]

## Skill Version(s):

1.0.5 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
