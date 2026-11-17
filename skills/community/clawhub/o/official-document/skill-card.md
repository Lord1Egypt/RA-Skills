## Description:

Generates Chinese official government documents in DOCX format using GB/T 9704-2012 layout, typography, spacing, page numbering, attachments, sign-off, and contact conventions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangxue1985122219](https://clawhub.ai/user/zhangxue1985122219)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to prepare standardized Chinese official documents such as notices, requests, reports, and letters. The skill is most useful when a user needs a structured DOCX document with GB/T 9704-2012 formatting from supplied document metadata and body content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated DOCX files may include personal contact details or other sensitive document content.

Mitigation: Review all contact details and document content before producing or sharing the DOCX.

Risk: The skill depends on python-docx for local document generation.

Mitigation: Use a virtual environment and hash-verified dependency installation when stricter supply-chain control is required.

## Reference(s):

- [GB/T 9704-2012 党政机关公文格式](references/gbt9704-2012.md)
- [ClawHub skill page](https://clawhub.ai/zhangxue1985122219/skills/official-document)

## Skill Output:

**Output Type(s):** [Guidance, Configuration, Code, Shell commands, Files]

**Output Format:** [Markdown guidance with Python configuration examples and shell commands; generated output is a DOCX file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python-docx and local review of generated document content before sharing.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
