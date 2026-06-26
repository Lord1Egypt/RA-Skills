## Description: <br>
Image to Markdown - extract text from images (PNG, JPG, WebP) to Markdown with OCR. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tanis90](https://clawhub.ai/user/tanis90) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agents use Pic2md to extract OCR text from screenshots, photos, scanned pages, local image files, or image URLs and return the result as Markdown. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected screenshots, photos, or scanned documents are uploaded to MinerU's cloud service for OCR processing. <br>
Mitigation: Use the skill only for images that are appropriate to send to MinerU, and avoid confidential content unless MinerU's handling and retention claims satisfy the user's requirements. <br>
Risk: The optional higher-precision or batch workflow can require authentication with MinerU. <br>
Mitigation: Use authenticated MinerU modes only when the user understands the account access and operational implications. <br>
Risk: OCR output may be incomplete or inaccurate for low-quality images or unsupported language settings. <br>
Mitigation: Review extracted Markdown against the source image before relying on it, and pass an explicit language hint when needed. <br>


## Reference(s): <br>
- [Pic2md ClawHub release](https://clawhub.ai/tanis90/pic2md) <br>
- [MinerU](https://mineru.net) <br>
- [MinerU CLI ecosystem](https://mineru.net/ecosystem?tab=cli) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown text with optional CLI command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces OCR-derived Markdown from selected image inputs; image processing is delegated to MinerU's cloud API.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
