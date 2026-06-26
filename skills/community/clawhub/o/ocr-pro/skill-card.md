## Description: <br>
Ocr Pro helps agents extract text and layout-aware content from PDFs and images using MinerU, including VLM support for complex layouts, tables, figures, scans, photos, and screenshots. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mzlzyca](https://clawhub.ai/user/mzlzyca) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and operations teams use Ocr Pro to extract text and layout-aware content from PDFs, scanned documents, screenshots, photos, and other images through MinerU. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Documents or URLs may be processed by MinerU/OpenDataLab rather than locally. <br>
Mitigation: Avoid confidential, regulated, internal, or customer documents unless the organization approves the service and its retention and privacy terms. <br>
Risk: MINERU_TOKEN exposure could allow unauthorized use of the configured MinerU account. <br>
Mitigation: Keep MINERU_TOKEN private, avoid committing it to files or logs, and rotate it if exposed. <br>


## Reference(s): <br>
- [Ocr Pro on ClawHub](https://clawhub.ai/mzlzyca/ocr-pro) <br>
- [MinerU](https://mineru.net) <br>
- [MinerU API Token Management](https://mineru.net/apiManage/token) <br>
- [MinerU GitHub Repository](https://github.com/opendatalab/MinerU) <br>
- [mineru-open-api Go Package](https://github.com/opendatalab/MinerU-Ecosystem/cli/mineru-open-api) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Files, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and OCR output paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write extracted OCR results to an output directory; token-based authentication is required with MINERU_TOKEN or mineru-open-api auth.] <br>

## Skill Version(s): <br>
0.4.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
