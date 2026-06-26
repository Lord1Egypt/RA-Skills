## Description: <br>
Recognizes Alipay and WeChat mobile payment bill images or PDFs and extracts structured transaction fields such as time, merchant, amount, and transaction type. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scnet-sugon](https://clawhub.ai/user/scnet-sugon) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to send a local mobile payment bill image or PDF to Scnet OCR and receive structured transaction data for review, reconciliation, or downstream processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Payment bill images or PDFs may contain sensitive financial data and are uploaded to Scnet's external OCR service. <br>
Mitigation: Confirm the exact file path before each run, avoid uploading unrelated or unredacted financial records, and review the provider's privacy, retention, and compliance terms before using real payment data. <br>
Risk: The skill requires a Scnet API credential. <br>
Mitigation: Store SCNET_API_KEY in an environment variable or local config file with restricted permissions, and do not paste the key into chat or commit it to source control. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/scnet-sugon/mobile-pay-bill-ocr) <br>
- [Sugon-Scnet OCR API Docs](references/api-docs.md) <br>
- [Mobile Payment Bill Fields Summary](assets/templates/fields-summary.md) <br>
- [Scnet Website](https://www.scnet.cn) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Text, Shell commands, Configuration instructions] <br>
**Output Format:** [Structured JSON with OCR recognition results; text error messages on failure.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SCNET_API_KEY and a local file path; supported input includes common image formats and PDFs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, SKILL.md frontmatter, skill.yaml, CHANGELOG.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
