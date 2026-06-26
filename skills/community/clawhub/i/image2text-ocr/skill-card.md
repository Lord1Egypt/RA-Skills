## Description: <br>
Extracts text from user-specified images, PDFs, or archives by sending the file to the Scnet OCR service and returning structured OCR results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scnet-sugon](https://clawhub.ai/user/scnet-sugon) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to run OCR on local image, PDF, or archive files and receive structured recognition results for downstream processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected images, PDFs, or archives are uploaded to Scnet for OCR and may contain sensitive information. <br>
Mitigation: Use the skill only for files approved for Scnet processing, and avoid highly sensitive documents unless Scnet's privacy and retention terms meet the deployment requirements. <br>
Risk: The skill requires a Scnet API key and reads credentials from local configuration. <br>
Mitigation: Use a dedicated API key where possible, do not paste keys into chat, and keep config/.env permissions restrictive. <br>
Risk: The skill depends on Python requests and network access to the Scnet OCR API. <br>
Mitigation: Install dependencies from a trusted package source and verify network access, timeout behavior, and retry limits before deployment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/scnet-sugon/image2text-ocr) <br>
- [Scnet Website](https://www.scnet.cn) <br>
- [Sugon-Scnet OCR API Documentation Summary](references/api-docs.md) <br>
- [OCR Field Summary](assets/templates/fields-summary.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration] <br>
**Output Format:** [JSON emitted to standard output, with text error messages for configuration, credential, file, network, and API failures.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SCNET_API_KEY and accepts an OCR type plus a local file path.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata, SKILL.md frontmatter, skill.yaml, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
