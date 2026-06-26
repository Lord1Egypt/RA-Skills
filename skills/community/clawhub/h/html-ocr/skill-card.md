## Description: <br>
Extracts searchable Markdown text from images and scanned content embedded in local HTML files using MinerU OCR. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mzlzyca](https://clawhub.ai/user/mzlzyca) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, archivists, and accessibility workflows use this skill to turn image-heavy or scanned HTML pages into searchable text or Markdown using MinerU OCR. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected HTML and embedded images may be processed by MinerU, a third-party service. <br>
Mitigation: Use this skill only for content whose data handling is acceptable; avoid confidential, regulated, or proprietary HTML unless MinerU processing is approved. <br>
Risk: A MinerU token can authorize OCR API access if exposed. <br>
Mitigation: Use a revocable token, keep MINERU_TOKEN out of prompts and logs, and rotate the token if exposure is suspected. <br>
Risk: OCR results from image-heavy or mixed-content pages may be incomplete or inaccurate. <br>
Mitigation: Review extracted Markdown before relying on it, and use VLM mode for complex pages when higher OCR quality is needed. <br>


## Reference(s): <br>
- [ClawHub HTML OCR release](https://clawhub.ai/mzlzyca/html-ocr) <br>
- [MinerU](https://mineru.net) <br>
- [MinerU token management](https://mineru.net/apiManage/token) <br>
- [OpenDataLab MinerU repository](https://github.com/opendatalab/MinerU) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown or plain text extracted by the MinerU CLI, with shell command guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires mineru-open-api and MINERU_TOKEN; local HTML input is processed by MinerU.] <br>

## Skill Version(s): <br>
0.4.0 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
