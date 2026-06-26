## Description: <br>
Image To Markdown extracts text from image files and URLs into Markdown using MinerU Open API OCR. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tanis90](https://clawhub.ai/user/tanis90) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agents use this skill to read screenshots, photos, scanned pages, and other image files or image URLs, then return the extracted text as Markdown. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uploads image content to MinerU's cloud API for OCR processing. <br>
Mitigation: Do not submit sensitive, regulated, or confidential images unless use of MinerU's cloud service is approved for that data. <br>
Risk: OCR results can omit, reorder, or misread text, especially from low-quality images or an incorrect language hint. <br>
Mitigation: Review extracted Markdown against the source image before using it for decisions, records, or downstream automation. <br>
Risk: The skill depends on the external mineru-open-api CLI and local installation paths. <br>
Mitigation: Install the CLI from the documented package source and confirm `mineru-open-api flash-extract --help` works before relying on the skill. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/tanis90/image-to-markdown) <br>
- [MinerU homepage](https://mineru.net) <br>
- [MinerU CLI download](https://mineru.net/ecosystem?tab=cli) <br>
- [MinerU Open API Go package](https://github.com/opendatalab/MinerU-Ecosystem) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown text with optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [OCR output depends on image quality, the selected language hint, and the 10MB image size limit.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
