## Description:

Turns an inbound B2B manufacturing RFQ or sourcing inquiry into a structured spec sheet, missing-information clarification checklist, and professional English reply draft without inventing prices, MOQs, lead times, certifications, stock, or test data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fly0pants](https://clawhub.ai/user/fly0pants)

### License/Terms of Use:

MIT-0

## Use Case:

Sales and engineering teams at OEM/ODM manufacturers use this skill to turn inbound sourcing and quote requests into a confirmed spec sheet, targeted clarification questions, and a buyer-facing English reply draft. It is intended for custom-manufactured products where pricing, MOQ, lead time, certifications, compatibility, and test data must be verified before being promised.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated replies could become commercially misleading if unverified prices, MOQs, lead times, certifications, compatibility claims, stock, or test data are sent as facts.

Mitigation: Review every generated reply before sending and keep unverified commercial or technical details as clarification questions or to-confirm next steps.

Risk: Buyer-provided RFQ text or fields may be untrusted, especially when reused in Markdown output.

Mitigation: Treat script output as a draft and avoid rendering untrusted RFQ fields in viewers that automatically load remote content.

Risk: Globally installed CLI tooling can drift from the reviewed version.

Mitigation: Pin any CLI tooling used to install or run the skill in production workflows.

## Reference(s):

- [This skill on ClawHub](https://clawhub.ai/fly0pants/skills/oem-rfq-assistant)
- [Canonical RFQ field list](artifact/references/rfq-fields.md)
- [Never-fabricate red lines](artifact/references/compliance.md)
- [English reply templates](artifact/references/reply-templates.md)
- [ChiZe official website](https://chizeparts.com/)
- [ChiZe OEM/ODM services](https://chizeparts.com/oem-odm/)
- [ChiZe RFQ checklist guide](https://chizeparts.com/knowledge/custom-saddle-rfq-checklist/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with a spec sheet table, grouped clarification checklist, reply draft, and optional Markdown brief generated from JSON RFQ fields.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The helper script accepts structured RFQ JSON from a file or stdin and renders missing values as to-confirm items.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
