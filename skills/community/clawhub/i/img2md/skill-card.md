## Description: <br>
Image to Markdown - extract text from images (PNG, JPG, WebP) to Markdown with OCR. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tanis90](https://clawhub.ai/user/tanis90) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, agents, and other users use Img2md to extract text from screenshots, photos, scanned pages, local image files, or image URLs and return the result as Markdown. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected images are uploaded to MinerU's cloud OCR service for processing, which may expose confidential screenshots, documents, IDs, or private business images. <br>
Mitigation: Use the skill only with images approved for cloud processing, and avoid confidential or regulated content unless that processing is acceptable for the use case. <br>
Risk: OCR output may be incomplete or inaccurate, especially for low-quality images, complex layouts, or language settings that do not match the source. <br>
Mitigation: Review the extracted Markdown against the source image and use the CLI language hint or higher-precision MinerU extraction flow when accuracy requirements are higher. <br>


## Reference(s): <br>
- [ClawHub Img2md skill page](https://clawhub.ai/tanis90/img2md) <br>
- [MinerU](https://mineru.net) <br>
- [MinerU CLI ecosystem](https://mineru.net/ecosystem?tab=cli) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown text with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses mineru-open-api for OCR; selected images may be uploaded to MinerU's cloud OCR service and are limited to 10MB.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.json release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
