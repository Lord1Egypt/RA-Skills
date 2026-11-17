## Description:

Xiangyun Platform Passport OCR Skill calls the Xiangyun API to perform structured recognition of passport images and extract fields such as passport number, name, sex, dates, issuing authority, and nationality.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liudengkui](https://clawhub.ai/user/liudengkui)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to submit passport images or Base64 data to Xiangyun/netocr OCR, review structured passport fields, and export cached results when requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Passport images and extracted passport fields are sensitive personal data that may be sent to Xiangyun/netocr.

Mitigation: Use the skill only when authorized to process and upload those documents, and confirm the user's consent before API submission.

Risk: Extracted passport data may be written locally as cached JSON or exported files.

Mitigation: Use no-save behavior for sensitive documents, avoid shared or synced folders, and retain exported files only as long as needed.

Risk: API credentials may be stored locally and could be exposed if printed, logged, or shared.

Mitigation: Rotate credentials after exposure and consider masking secrets, restricting file permissions, and reviewing credential handling before deployment.

## Reference(s):

- [Xiangyun Passport Recognition API Reference](references/api_docs.md)
- [Xiangyun Product Page](https://www.netocr.com/products.html)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance]

**Output Format:** [Markdown tables, JSON OCR results, and optional CSV, Excel, or JSON export files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write cached OCR JSON next to source images unless no-save behavior is used; exports occur only on explicit request.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
