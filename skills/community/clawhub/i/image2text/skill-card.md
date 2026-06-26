## Description: <br>
Extract text from images using tesseract OCR, supporting local files, URLs, and base64 inputs for text-only AI models without vision capability. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[caiming0331](https://clawhub.ai/user/caiming0331) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to extract text from receipts, screenshots, document images, local image files, web image URLs, or base64 image data when the active model does not have vision capability. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: URL inputs can cause outbound network requests from the machine running the agent. <br>
Mitigation: Prefer local files or trusted public URLs, and avoid localhost, private-network, or metadata-service URLs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/caiming0331/image2text) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text OCR output, optionally wrapped between RAW_TEXT markers] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires tesseract and selected language packs on the machine running the agent.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
