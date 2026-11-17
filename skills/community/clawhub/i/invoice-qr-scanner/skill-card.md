## Description:

Scan QR codes from invoice receipts and automatically fill electronic invoice applications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenzhuowen](https://clawhub.ai/user/chenzhuowen)

### License/Terms of Use:

MIT

## Use Case:

Employees and business users use this skill to decode QR codes from invoice receipt images, open the linked electronic invoicing form, and fill required company and contact details for review and submission.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: QR-derived invoice links may direct the agent to an untrusted or unexpected destination.

Mitigation: Confirm the destination domain before browser actions and use the skill only with trusted invoice QR codes.

Risk: Invoice forms can involve sensitive company, tax, bank, phone, and email data.

Mitigation: Require final user review before entering or submitting sensitive data, and avoid retaining bank account details in general memory unless the user explicitly accepts cross-session retention.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenzhuowen/skills/invoice-qr-scanner)
- [OpenClaw documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and browser-action guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include decoded QR URLs, form-filling status, requested missing fields, and submission review notes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
