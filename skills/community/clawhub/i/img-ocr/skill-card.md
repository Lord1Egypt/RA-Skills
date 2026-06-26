## Description: <br>
This skill extracts Chinese and English text from image files using Tesseract OCR. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ginntech](https://clawhub.ai/user/ginntech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, employees, and external users use this skill to extract text from screenshots or local image files when an agent needs OCR assistance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Dependency installation uses pip and sudo apt steps. <br>
Mitigation: Review dependency installation commands before use and install only from trusted package sources in an appropriate environment. <br>
Risk: OCR can expose sensitive text from screenshots or images into the agent workflow. <br>
Mitigation: Avoid processing images that contain secrets, credentials, personal data, or confidential text unless the workflow is approved for that data. <br>
Risk: The skill depends on a correct local image path and installed Tesseract language data. <br>
Mitigation: Verify the image path and OCR dependencies before running, including the Chinese simplified language pack when Chinese recognition is needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ginntech/img-ocr) <br>
- [Publisher profile](https://clawhub.ai/user/ginntech) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text extracted from an image, with shell command examples when setup or execution guidance is needed.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local image path, Python dependencies, Tesseract OCR, and the Chinese simplified language pack for Chinese text.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
