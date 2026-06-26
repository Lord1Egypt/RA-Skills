## Description: <br>
Scans QR codes from invoice receipt images and helps an agent fill electronic invoice application forms with stored company and contact details. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenzhuowen](https://clawhub.ai/user/chenzhuowen) <br>

### License/Terms of Use: <br>
MIT License <br>


## Use Case: <br>
Employees or external users who manage electronic invoicing use this skill to decode receipt QR codes, open invoice application sites, and prepare invoice forms with company and recipient details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The decoded QR URL may lead to an untrusted invoice site that receives company, tax, banking, phone, or email details. <br>
Mitigation: Require the agent to show the decoded domain, confirm it is trusted, display every field to be submitted, and get explicit approval before submitting. <br>
Risk: Stored invoice details can expose sensitive company or banking information during form filling. <br>
Mitigation: Avoid storing bank account details unless necessary and review memory-derived values before they are used in browser forms. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chenzhuowen/invoice-qr-scanner) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and short status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include decoded invoice URLs and form-field values for user review before submission.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
