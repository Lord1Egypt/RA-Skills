## Description:

Calls the Xiangyun API (typeId=17) to perform structured bank card OCR from local files or Base64 image input, extracting card number, card type, card name, issuing bank, and bank code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liudengkui](https://clawhub.ai/user/liudengkui)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to recognize bank card details from images through the Xiangyun OCR service and optionally export recognized records for follow-up processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bank-card images and OCR results may contain sensitive payment-card data and are sent to Xiangyun/netocr.com for recognition.

Mitigation: Use the skill only where uploading those images to the OCR provider is approved; prefer test or non-production card images when validating behavior.

Risk: OCR credentials are stored locally in config.json.

Mitigation: Protect the skill directory, avoid committing config.json with live credentials, and reset or rotate credentials when access is no longer needed.

Risk: Successful local-file recognition may save JSON results beside source images.

Mitigation: Run recognition with --no-save when cached results are unnecessary, and protect or delete generated JSON files after use.

Risk: Exported CSV or Excel files may contain sensitive OCR fields or spreadsheet formula-like values.

Mitigation: Sanitize exported data before opening or sharing spreadsheets, and avoid opening exports from untrusted inputs.

## Reference(s):

- [Xiangyun Bank Card OCR API documentation](artifact/references/api_docs.md)
- [Xiangyun bank card OCR product page](https://www.netocr.com/bankCard.html)
- [Xiangyun platform](https://www.netocr.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with shell commands; recognition results as JSON or tables, with optional CSV, Excel, or JSON exports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save per-image recognition JSON beside source images unless run with --no-save.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
