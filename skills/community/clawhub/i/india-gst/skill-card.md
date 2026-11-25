## Description:

India GST toolkit - validate GSTINs offline (checksum, state, PAN), add or remove GST with the correct CGST+SGST/UTGST or IGST split, create Rule 46 compliant tax invoices and bills of supply as print-ready HTML, check registration/composition/e-invoice/e-way bill/HSN obligations, and list GSTR-1/3B due dates. Rules current to November 2026 (GST 2.0 slabs 5/18/40). Use for any Indian GST question, invoice, or GSTIN check.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sanketbhatia](https://clawhub.ai/user/sanketbhatia)

### License/Terms of Use:

MIT-0

## Use Case:

Freelancers, shops, and small businesses in India can use the skill to check GSTIN format and checksums, calculate GST, prepare print-ready invoices, review common compliance obligations, and find filing due dates. It provides calculation and format support rather than legal advice.

### Deployment Geography for Use:

India

## Known Risks and Mitigations:

Risk: The security review notes undeclared tool scope and file-writing capability; static analysis did not cover the sample PNG.

Mitigation: Review the skill's requested tool scope and generated-file paths before installation, and inspect the sample image if it is part of your review.

## Reference(s):

- [India GST Toolkit on ClawHub](https://clawhub.ai/sanketbhatia/skills/india-gst)
- [GST rules reference (November 2026)](references/rules.md)
- [CBIC GST portal](https://cbic-gst.gov.in/)
- [GST taxpayer search portal](https://services.gst.gov.in/)

## Skill Output:

**Output Type(s):** [Text, JSON, HTML files, Guidance]

**Output Format:** [JSON results, print-ready HTML invoices, and explanatory text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Works offline; invoice HTML can be printed or saved as PDF.]

## Skill Version(s):

1.0.0 (source: server-resolved ClawHub release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
