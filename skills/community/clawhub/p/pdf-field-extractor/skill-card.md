## Description: <br>
AI-assisted PDF field extraction skill that identifies document types, extracts text or OCR content, and produces structured Excel or JSON outputs for invoices, contracts, receipts, bank statements, licenses, ID documents, shipping forms, and general documents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qiji0802](https://clawhub.ai/user/qiji0802) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and workflow users use this skill to turn uploaded PDFs into structured fields for review, export, and batch processing. It is intended for document extraction tasks such as invoice capture, contract term extraction, receipt parsing, bank statement parsing, ID or license extraction, and custom field extraction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive PDF content such as IDs, contracts, invoices, or bank statements may be sent to an external AI API during field extraction. <br>
Mitigation: Use only documents approved for the configured provider, redact sensitive fields when possible, and prefer local-only processing or explicit privacy disclosure for sensitive workflows. <br>
Risk: The skill requires sensitive AI provider credentials for extraction calls. <br>
Mitigation: Use a scoped API key, avoid sharing credentials in prompts or files, and rotate keys if they may have been exposed. <br>
Risk: The server security verdict is suspicious because privacy warnings and consent controls are not prominent for sensitive document processing. <br>
Mitigation: Review before installing, confirm the configured API destination, and require clear user consent before processing regulated or confidential documents. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qiji0802/pdf-field-extractor) <br>
- [Document type identification reference](references/doc_types.md) <br>
- [AI field extraction prompt templates](references/prompts.md) <br>
- [Tier configuration and limits](scripts/tier_config.py) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Files, Configuration guidance] <br>
**Output Format:** [Excel (.xlsx), JSON, extracted text, and optional summary message content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use local OCR and a configured OpenAI-compatible AI provider; output availability and volume are governed by the configured tier limits.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
