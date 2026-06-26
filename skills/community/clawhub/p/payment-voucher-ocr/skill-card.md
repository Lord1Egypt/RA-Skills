## Description: <br>
Recognizes payment vouchers and returns structured fields such as payer, payment method, purpose, amount, and handler seal information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scnet-sugon](https://clawhub.ai/user/scnet-sugon) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to run Scnet OCR on payment voucher image, PDF, or archive files and extract structured payment details for review or downstream automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Payment vouchers and extracted OCR contents can contain sensitive financial or personal information. <br>
Mitigation: Upload only documents needed for the task and avoid unnecessary personal or financial details. <br>
Risk: The skill uploads the user-specified document to Scnet's OCR API for processing. <br>
Mitigation: Confirm the destination endpoint and review the provider's privacy and retention terms before using confidential or regulated records. <br>
Risk: The skill requires an API key for Scnet access. <br>
Mitigation: Store the API key in the configured environment or local config file, restrict file permissions, and do not paste credentials into chat. <br>


## Reference(s): <br>
- [Sugon-Scnet OCR API documentation summary](references/api-docs.md) <br>
- [Payment voucher field summary](assets/templates/fields-summary.md) <br>
- [Scnet website](https://www.scnet.cn) <br>
- [ClawHub release page](https://clawhub.ai/scnet-sugon/payment-voucher-ocr) <br>


## Skill Output: <br>
**Output Type(s):** [text] <br>
**Output Format:** [JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes OCR result data to standard output; user-facing errors are emitted as text.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter, skill.yaml, CHANGELOG released 2025-05-29, ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
