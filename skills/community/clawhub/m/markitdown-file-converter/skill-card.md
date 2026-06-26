## Description: <br>
Markitdown File Converter helps agents convert common document, spreadsheet, presentation, PDF, and image files into Markdown or structured JSON. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sqlskills](https://clawhub.ai/user/sqlskills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to convert user-provided files into Markdown or JSON for downstream review, extraction, summarization, or workflow automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install or change document-conversion dependencies automatically. <br>
Mitigation: Run it in an isolated environment and prefer reviewed, pinned, manually installed dependencies before handling important documents. <br>
Risk: OCR behavior can send document images to a preconfigured cloud OCR service. <br>
Mitigation: Do not process confidential documents unless cloud OCR is disabled, removed, or configured to a trusted endpoint. <br>
Risk: The artifact includes a preconfigured PaddleOCR access token. <br>
Mitigation: Replace or revoke the embedded token and provide credentials through environment variables or a managed secret store. <br>
Risk: Converted Markdown or JSON may contain OCR, table, formatting, or formula extraction errors. <br>
Mitigation: Review converted output before relying on it for records, decisions, or automated downstream actions. <br>


## Reference(s): <br>
- [ClawHub skill release page](https://clawhub.ai/sqlskills/markitdown-file-converter) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, guidance] <br>
**Output Format:** [Markdown, JSON, and command-line guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create converted output files and extracted image assets in a local output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
