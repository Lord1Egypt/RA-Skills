## Description: <br>
Image OCR extracts text and content from photos, screenshots, scanned documents, and other image files using MinerU. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mzlzyca](https://clawhub.ai/user/mzlzyca) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run MinerU OCR on local image files or image URLs, including screenshots, receipts, whiteboards, scanned documents, and multilingual images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Images submitted to MinerU OCR may contain sensitive text or visual content. <br>
Mitigation: Review image sensitivity before processing and use approved data-handling practices for confidential, regulated, or customer content. <br>
Risk: Token-based extract mode depends on MINERU_TOKEN credentials. <br>
Mitigation: Store the token securely, avoid logging it, and use least-privilege credential handling where practical. <br>
Risk: OCR results can be incomplete or inaccurate for low-quality images or complex layouts. <br>
Mitigation: Review extracted content before relying on it and use the documented OCR or VLM modes for difficult inputs. <br>


## Reference(s): <br>
- [Image OCR on ClawHub](https://clawhub.ai/mzlzyca/photo-ocr) <br>
- [MinerU](https://mineru.net) <br>
- [MinerU GitHub Repository](https://github.com/opendatalab/MinerU) <br>
- [MinerU Token Management](https://mineru.net/apiManage/token) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, HTML, LaTeX, Shell commands, Configuration guidance] <br>
**Output Format:** [OCR content emitted to stdout or saved files, with Markdown, HTML, JSON, and LaTeX formats available through MinerU.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local image files and image URLs are supported; MINERU_TOKEN is required for token-based extract mode.] <br>

## Skill Version(s): <br>
0.4.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
