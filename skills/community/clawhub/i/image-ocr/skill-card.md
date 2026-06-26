## Description: <br>
Extract text from images using Tesseract OCR <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Xejrax](https://clawhub.ai/user/Xejrax) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and other agent users use this skill to extract text from user-selected image files with local Tesseract OCR. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing OCR tooling from untrusted package sources could introduce supply-chain risk. <br>
Mitigation: Install Tesseract only from trusted operating system repositories. <br>
Risk: Images processed for OCR may contain sensitive text. <br>
Mitigation: Run OCR only on images whose contents are appropriate to process in the local agent session. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Xejrax/image-ocr) <br>
- [Publisher profile](https://clawhub.ai/user/Xejrax) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local Tesseract OCR on user-selected image files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
