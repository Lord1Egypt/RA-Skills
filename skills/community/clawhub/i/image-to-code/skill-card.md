## Description: <br>
Converts images containing text, formulas, headings, and figures into structured code-style document output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nidhov01](https://clawhub.ai/user/nidhov01) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and document-processing teams use this skill to convert screenshots or scanned technical documents into text output containing title calls, body text calls, formula calls, and image placeholders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Images are uploaded to Baidu OCR by default, which can expose confidential, customer, regulated, or proprietary content. <br>
Mitigation: Do not process sensitive images unless Baidu OCR is disabled or replaced with an approved provider; use the offline fallback where privacy requirements apply. <br>
Risk: The artifact contains embedded Baidu OCR credentials. <br>
Mitigation: Remove embedded credentials, rotate any exposed keys, and configure approved provider credentials outside source-controlled skill files. <br>
Risk: Dependency versions are not fully pinned for reviewable installation. <br>
Mitigation: Pin and review dependency versions before installing or deploying the skill. <br>
Risk: OCR and formula recognition can produce incorrect text or LaTeX, especially for complex formulas or lower-quality images. <br>
Mitigation: Review generated output before using it in downstream documents, reports, or automation. <br>


## Reference(s): <br>
- [Baidu AI Console](https://console.bce.baidu.com/ai/) <br>
- [Tesseract OCR Documentation](https://tesseract-ocr.github.io/) <br>
- [pytesseract API](https://github.com/madmaze/pytesseract) <br>
- [OpenCV Documentation](https://docs.opencv.org/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text containing code-style document calls, LaTeX formula strings, and Markdown image placeholders] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can print converted output to the terminal or write it to a text file; OCR and formula output may require manual review.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and artifact/metadata.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
