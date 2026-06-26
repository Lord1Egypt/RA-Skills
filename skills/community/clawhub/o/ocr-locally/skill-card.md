## Description: <br>
OCR Locally extracts text from images and PDFs on macOS using native Vision and PDFKit frameworks without requiring network access or third-party libraries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ltryee](https://clawhub.ai/user/ltryee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run local OCR on user-selected screenshots, image files, and PDFs. The skill helps extract readable text, confidence details, and bounding-box metadata without sending files to an external OCR service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bundled Swift scripts execute locally on macOS against user-selected files. <br>
Mitigation: Review the scripts before use and run them only on macOS 10.15+ with files you intentionally provide. <br>
Risk: Saved OCR results can contain sensitive plaintext from images or documents. <br>
Mitigation: Choose safe output paths, limit sharing of generated text and confidence files, and delete them when no longer needed. <br>


## Reference(s): <br>
- [Local OCR Skill - Detailed Usage Guide](references/usage.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Files, Shell commands, Guidance] <br>
**Output Format:** [Plain text, JSON, or Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can save extracted text and confidence details to files; JSON output includes text blocks, confidence scores, and bounding boxes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
