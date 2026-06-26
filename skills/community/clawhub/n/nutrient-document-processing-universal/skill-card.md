## Description: <br>
Universal Nutrient DWS document-processing skill for Agent Skills-compatible products that helps agents convert PDF, Office, HTML, and image files, run OCR, extract text and data, redact PII, watermark, sign, fill forms, merge, split, reorder, and check API usage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jdrhyne](https://clawhub.ai/user/jdrhyne) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agent users use this skill to connect supported agents to Nutrient DWS document-processing workflows through an MCP server or direct API calls. It is suited for user-selected document conversion, OCR, extraction, redaction, signing, form filling, page operations, and usage checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-selected documents are sent to Nutrient's cloud API for processing and may contain sensitive data. <br>
Mitigation: Use the skill only when Nutrient's data handling policies are acceptable for the document contents, and review files before OCR, extraction, redaction, signing, or batch operations. <br>
Risk: API keys may be exposed if placed in broadly readable shell history or MCP configuration files. <br>
Mitigation: Use a dedicated Nutrient API key when possible and protect any environment files or MCP configuration files that contain credentials. <br>
Risk: MCP server mode can access files made available to its configured working directory. <br>
Mitigation: Set SANDBOX_PATH to a narrow work directory that contains only the documents intended for processing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jdrhyne/nutrient-document-processing-universal) <br>
- [Nutrient DWS Processor API](https://www.nutrient.io/api/) <br>
- [Nutrient DWS Processor guides](https://www.nutrient.io/guides/dws-processor/) <br>
- [Nutrient Processor API playground](https://dashboard.nutrient.io/processor-api/playground/) <br>
- [Skill repository](https://github.com/PSPDFKit-labs/nutrient-agent-skill) <br>
- [Nutrient DWS MCP server repository](https://github.com/PSPDFKit/nutrient-dws-mcp-server) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, code] <br>
**Output Format:** [Markdown with JSON configuration examples and inline shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce MCP configuration snippets, curl commands, API instruction JSON, and document-processing workflow guidance.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
