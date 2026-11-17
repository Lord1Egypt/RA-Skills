## Description:

Helps agents extract structured data from Malaysian and Singaporean invoices and receipts with SST/GST-aware fields, multilingual guidance, and a paid tax-rate retrieval step.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wms2537](https://clawhub.ai/user/wms2537)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to guide invoice and receipt data extraction for Malaysia and Singapore, including tax type detection, currency selection, line-item fields, and totals. The release also includes a paid endpoint that charges through SkillPay and returns current tax-rate values.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The paid endpoint sends a user identifier and may charge a caller-supplied user ID.

Mitigation: Install only where SkillPay independently authenticates users and prevents duplicate or unauthorized charges.

Risk: The endpoint primarily returns tax rates after billing rather than performing invoice OCR or structured parsing.

Mitigation: Use the skill's extraction guidance with an agent's own document parsing capability and verify parsed invoice results before relying on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wms2537/skills/my-sg-invoice-parser)
- [Homepage](https://github.com/swmeng/myskills)

## Skill Output:

**Output Type(s):** [guidance, JSON, API calls]

**Output Format:** [Markdown instructions with JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SKILLPAY_API_KEY for the paid billing and tax-rate endpoint.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
