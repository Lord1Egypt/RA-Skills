## Description:

JD Lawsuit Skill helps agents collect e-commerce order evidence, build local evidence bundles, and draft refund, 12315 complaint, and civil complaint documents for Chinese consumer disputes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaoyaner0201](https://clawhub.ai/user/xiaoyaner0201)

### License/Terms of Use:

MIT-0

## Use Case:

External users and assisting agents use this skill to organize Chinese e-commerce consumer-dispute evidence and prepare complaint or lawsuit-oriented documents. It is aimed at refund, product-quality, delivery, false-advertising, after-sale, and food-safety disputes.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The skill may expose sensitive order, payment, logistics, chat, invoice, and legal-document data while viewing logged-in pages and creating local evidence files.

Mitigation: Use only when the user accepts that access, redact addresses, phone numbers, IDs, tracking numbers, payment details, and unrelated chat content, store evidence privately, and delete bundles when no longer needed.

Risk: Generated complaint and lawsuit documents are templates and may not fit complex, high-value, or jurisdiction-sensitive disputes.

Mitigation: Have the user review and edit all generated documents, and recommend professional legal advice for larger or complex matters.

## Reference(s):

- [Platform Guide](references/platform-guide.md)
- [Evidence Collection](references/evidence-collection.md)
- [Legal Templates](references/legal-templates.md)
- [Legal Basis](references/legal-basis.md)
- [Complaint Channels](references/complaint-channels.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, guidance, files]

**Output Format:** [Markdown documents and evidence indexes, JSON order data, screenshot/PDF evidence bundles, and text guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [When used as documented, evidence is saved under ~/Downloads/dispute-evidence/{orderId}/.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
