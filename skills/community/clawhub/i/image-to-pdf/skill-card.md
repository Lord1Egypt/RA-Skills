## Description: <br>
Merges multiple images into a single PDF, supports Excel-based PDF renaming, and provides OCR guidance for scanned PDFs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[meowlegemy-sudo](https://clawhub.ai/user/meowlegemy-sudo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
People processing accounting vouchers or scanned documents use this skill to merge and rotate image pages into PDFs, rename PDFs from an Excel voucher list, and extract text from scanned PDFs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send sensitive document outputs and metadata to Telegram automatically without clear per-use confirmation. <br>
Mitigation: Keep processing local unless Telegram delivery is explicitly intended, and verify the recipient before each send. <br>
Risk: Voucher, company, or ship details may appear in filenames or outbound messages. <br>
Mitigation: Avoid placing sensitive details in filenames or messages unless they are required and approved for the workflow. <br>
Risk: OCR workflows can leave temporary files containing document images or extracted text. <br>
Mitigation: Delete OCR temporary files after processing, especially when handling confidential documents. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/meowlegemy-sudo/image-to-pdf) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local PDF and OCR workflow guidance; Telegram delivery should be used only when explicitly intended.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, created 2026-03-06) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
