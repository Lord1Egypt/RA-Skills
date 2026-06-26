## Description: <br>
Uses the MinerU API to parse PDF, Word, PowerPoint, and image files into Markdown with support for formulas, tables, and OCR. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[EasonAI-5589](https://clawhub.ai/user/EasonAI-5589) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, researchers, and document-processing teams use this skill to call MinerU for extracting structured Markdown, tables, formulas, OCR text, and layout outputs from supported document formats. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Documents processed with this skill are sent to MinerU's external cloud service. <br>
Mitigation: Use only documents approved for cloud processing and avoid confidential, regulated, or proprietary files unless privacy and retention terms have been reviewed. <br>
Risk: The MinerU API token can authorize external processing requests if exposed. <br>
Mitigation: Store MINERU_TOKEN securely, avoid committing it to files or logs, and rotate it if exposure is suspected. <br>


## Reference(s): <br>
- [MinerU website](https://mineru.net/) <br>
- [MinerU API documentation](https://mineru.net/apiManage/docs) <br>
- [MinerU GitHub repository](https://github.com/opendatalab/MinerU) <br>
- [ClawHub skill page](https://clawhub.ai/EasonAI-5589/mineru) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and JSON API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance includes MinerU API task submission, polling, batch upload, environment variable setup, and expected output files.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
