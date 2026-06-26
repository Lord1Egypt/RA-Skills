## Description: <br>
Use this skill to extract structured Markdown and JSON from PDFs and document images, including tables, formulas, figures, charts, headers, footers, multi-column layouts, and reading order. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bobholamovic](https://clawhub.ai/user/bobholamovic) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and document-processing teams use this skill to call the PaddleOCR CLI for structured parsing of complex PDFs and document images into Markdown and JSON outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Documents selected for parsing may be processed by PaddleOCR's remote API. <br>
Mitigation: Confirm data-sharing, retention, and compliance terms before processing confidential, regulated, financial, legal, or customer documents. <br>
Risk: The skill depends on a PaddleOCR access token and the installed PaddleOCR CLI package. <br>
Mitigation: Install only from trusted package sources, keep the access token secret, and handle authentication, quota, and no-content errors explicitly. <br>


## Reference(s): <br>
- [PaddleOCR Official API CLI Documentation](https://www.paddleocr.ai/latest/en/version3.x/inference_deployment/serving/paddleocr_official_api/cli.html) <br>
- [ClawHub skill release page](https://clawhub.ai/bobholamovic/paddleocr-doc-parsing) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON output examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the paddleocr CLI and PADDLEOCR_ACCESS_TOKEN; may return extracted page Markdown plus image resource links.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
