## Description:

Generate professional PDF invoices from JSON data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tmigone](https://clawhub.ai/user/tmigone)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to turn structured invoice JSON into PDF invoices for billing documents, payment requests, and saved client invoice templates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The core PDF rendering path uses a vulnerable Handlebars dependency.

Mitigation: Upgrade or verify the Handlebars dependency before processing customer, tax, or billing data.

Risk: The script references assets/invoice.hbs, but that template was not present in the inspected artifact.

Mitigation: Confirm the template is supplied and reviewed before relying on invoice generation.

Risk: Generated invoices can contain sensitive customer and billing information.

Mitigation: Use an INVOICE_DIR location with appropriate access controls and avoid testing with real billing data until dependencies and templates are verified.

## Reference(s):

- [Invoice Data Schema](references/data-schema.md)
- [ClawHub Skill Page](https://clawhub.ai/tmigone/skills/invoice-generator)
- [Publisher Profile](https://clawhub.ai/user/tmigone)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands; the runtime script produces a PDF invoice file path.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires structured invoice JSON, INVOICE_DIR, Node.js dependencies, jq, and weasyprint.]

## Skill Version(s):

1.0.0 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
