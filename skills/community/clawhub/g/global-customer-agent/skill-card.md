## Description:

Provides 24/7 multilingual customer reception for cross-border commerce by understanding customer needs, recommending products, and drafting multilingual quotations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangm-a3](https://clawhub.ai/user/wangm-a3)

### License/Terms of Use:

MIT-0

## Use Case:

External customer-service and sales teams use this skill to receive multilingual inquiries, classify customer needs, recommend products, and draft localized quotes for cross-border commerce workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic customer replies or quote drafts could be sent with incorrect pricing, inventory, or sensitive content.

Mitigation: Require human approval before sending quotes or sensitive replies, especially before connecting the skill to live customer channels, pricing, inventory, or CRM systems.

Risk: Unclear customer-data boundaries could expose more CRM or customer information than the workflow needs.

Mitigation: Define the customer data the skill may access and limit integrations to those approved data fields.

Risk: Language detection errors, mistranslations, or pricing mistakes could mislead customers.

Mitigation: Add fallback rules for uncertain language detection, pricing errors, and mistranslations.

## Reference(s):

- [Customer Lifecycle Reference](references/customer-lifecycle.md)
- [ClawHub Skill Page](https://clawhub.ai/wangm-a3/skills/global-customer-agent)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown and plain text customer-response drafts, quote outlines, product-recommendation guidance, and lifecycle-management guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only skill; no executable tool or API integration is included in the artifact.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
