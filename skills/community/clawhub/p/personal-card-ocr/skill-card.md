## Description: <br>
Extracts text and structured fields from images of personal documents, cards, and certificates using the Scnet OCR API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scnet-sugon](https://clawhub.ai/user/scnet-sugon) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to send a local image or document file to Scnet OCR and receive structured OCR fields for supported personal cards, identity documents, bank cards, certificates, and related records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can process passports, IDs, bank cards, birth certificates, and similar sensitive records through an external OCR service. <br>
Mitigation: Use only when authorized to send the document image to Scnet, confirm user consent before each upload, and avoid broad automatic use for generic OCR. <br>
Risk: OCR output may contain sensitive personal and financial data. <br>
Mitigation: Limit downstream sharing, storage, and logging of returned JSON to what the use case requires. <br>
Risk: The skill requires a Scnet API key. <br>
Mitigation: Store SCNET_API_KEY outside chat and source control, rotate expired keys, and restrict access to the local configuration file. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/scnet-sugon/personal-card-ocr) <br>
- [Scnet website](https://www.scnet.cn) <br>
- [Sugon-Scnet OCR API docs](references/api-docs.md) <br>
- [OCR fields summary](assets/templates/fields-summary.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration, shell commands] <br>
**Output Format:** [JSON returned on stdout with structured OCR fields; errors are human-readable text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SCNET_API_KEY and uploads the provided file to the external Scnet OCR service.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
