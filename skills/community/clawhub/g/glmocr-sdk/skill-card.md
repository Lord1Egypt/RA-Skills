## Description: <br>
GLM-OCR-SDK helps agents extract text, tables, formulas, and structured regions from document images, PDFs, and scans using the GLM-OCR SDK. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jaredforreal](https://clawhub.ai/user/jaredforreal) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to parse invoices, scanned pages, reports, screenshots, and other document-like files into Markdown and structured JSON for downstream review, summarization, or data extraction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Documents and OCR inputs may be sent to Zhipu's cloud service when using MaaS mode. <br>
Mitigation: Use the skill only for documents approved for that service, and avoid confidential inputs unless cloud OCR use is authorized. <br>
Risk: The ZHIPU_API_KEY credential is required for MaaS mode and may be exposed if passed or stored carelessly. <br>
Mitigation: Prefer environment variables or a protected secret store, avoid command-line key exposure where possible, and do not commit .env files. <br>
Risk: The skill depends on the external glmocr package. <br>
Mitigation: Verify the glmocr package source before installing and use trusted package indexes or pinned versions when deploying. <br>


## Reference(s): <br>
- [GLM-OCR SDK skill source](https://github.com/zai-org/GLM-OCR/tree/main/skills/sdk) <br>
- [ClawHub skill page](https://clawhub.ai/jaredforreal/glmocr-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Files, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown and JSON, with optional saved JSON, Markdown, cropped images, and layout visualization files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ZHIPU_API_KEY for MaaS mode; CLI and Python API paths are documented.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
