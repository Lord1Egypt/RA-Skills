## Description:

Audits hospital surgical logs against billing to find revenue leakage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[srikanth-hn](https://clawhub.ai/user/srikanth-hn)

### License/Terms of Use:


## Use Case:

External healthcare billing or revenue-cycle staff can use this skill to compare surgical notes or procedure summaries against billed items, identify potentially missed charges, and draft a concise administrator approval request.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill works with hospital logs that may contain patient-identifying, clinical, or billing-sensitive information.

Mitigation: Use it only when authorized to process the data, minimize unnecessary clinical detail in outputs, and follow the organization's healthcare data handling policies.

Risk: Generated discrepancy reports and WhatsApp drafts may include incorrect billing interpretations or sensitive information.

Mitigation: Have a qualified reviewer check the report and draft before sharing, and use an approved communication channel for healthcare or billing information.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown report with a discrepancy table, estimated leakage total, and message draft]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires review before sharing because source data and generated drafts may contain sensitive healthcare or billing information.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
