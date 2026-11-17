## Description:

Add password protection and encryption to a PDF. Supports AES-256, AES-128, RC4-128 encryption and granular permissions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rishabhdugar](https://clawhub.ai/user/rishabhdugar)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to call the PDF API Hub service to password-protect PDFs, choose an encryption mode, and set document permissions before sharing or storing files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive PDFs and passwords are sent to a third-party processor.

Mitigation: Use the skill only when pdfapihub.com is approved for the relevant document class and its retention, access, and processing controls meet the user's requirements.

Risk: The skill supports legacy RC4 encryption.

Mitigation: Prefer AES-256 for normal use and avoid RC4 unless a documented compatibility requirement justifies it.

Risk: Private, regulated, or high-value PDFs may require additional review before external processing.

Mitigation: Review the provider and workflow before using the skill with regulated or sensitive documents.

## Reference(s):

- [PDF API Hub documentation](https://pdfapihub.com/docs)
- [PDF API Hub](https://pdfapihub.com)
- [ClawHub skill page](https://clawhub.ai/rishabhdugar/skills/lock-pdf)

## Skill Output:

**Output Type(s):** [API Calls, Files, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with JSON request examples and API response data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The API can return a locked PDF as a file, URL, or base64 payload.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
