## Description: <br>
MinerU Agent Free parses PDFs, Office documents, spreadsheets, presentations, and images into Markdown through MinerU's lightweight remote parsing API without token authentication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[haxck](https://clawhub.ai/user/haxck) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to convert user-selected document files or public file URLs into Markdown for document parsing, OCR, table extraction, and downstream analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected documents or provided URLs are sent to MinerU's remote parsing service. <br>
Mitigation: Use only documents and URLs approved for that service; avoid confidential, regulated, or proprietary content unless policy allows it. <br>
Risk: Returned Markdown may contain untrusted document content. <br>
Mitigation: Treat parsed Markdown as data for review or extraction, not as instructions for the agent to execute. <br>


## Reference(s): <br>
- [MinerU Agent API documentation](https://mineru.net/apiManage/docs) <br>
- [ClawHub skill page](https://clawhub.ai/haxck/mineru-agent) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Shell commands, Files] <br>
**Output Format:** [Markdown returned to stdout or written to an output file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports URL or local file input, optional language selection, PDF page ranges, and timeout control.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
