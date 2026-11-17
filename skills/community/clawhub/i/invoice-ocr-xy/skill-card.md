## Description:

Scans PDF, OFD, and image invoice files, sends them to the Xianyun NetOCR invoice OCR API, and returns structured invoice recognition results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liudengkui](https://clawhub.ai/user/liudengkui)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to batch-recognize invoices for reimbursement, accounting, or document-processing workflows after configuring Xianyun NetOCR credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Invoice files can contain sensitive personal, tax, travel, medical, or payment information and are sent to netocr.com for OCR processing.

Mitigation: Use the skill only when that data transfer is acceptable for the user's policy and redact or exclude sensitive files when possible.

Risk: NetOCR credentials are required and may be exposed if pasted into chat or reused from a privileged account.

Mitigation: Use a dedicated low-privilege NetOCR credential and avoid sharing OCR secrets in conversation logs.

Risk: Runtime setup may install dependencies while exporting Excel results.

Mitigation: Run the skill in an isolated environment and install dependencies deliberately before processing invoices.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liudengkui/skills/invoice-ocr-xy)
- [Xianyun NetOCR website](https://netocr.com)
- [Xianyun OCR API reference](https://www.netocr.com/invoiceFor2.html)

## Skill Output:

**Output Type(s):** [Text, JSON, Files, Shell commands, Configuration guidance]

**Output Format:** [Markdown guidance with shell commands; invoice results as console text, JSON, or Excel files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Xianyun NetOCR credentials and sends invoice file contents to netocr.com for OCR processing.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
