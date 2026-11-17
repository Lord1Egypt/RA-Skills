## Description:

Provides agent guidance for processing documents with Nutrient DWS through the Nutrient MCP server or direct API calls, including conversion, OCR, extraction, redaction, watermarking, signing, page operations, form filling, and usage checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jdrhyne](https://clawhub.ai/user/jdrhyne)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document-automation teams use this skill to ask compatible agents to configure or call Nutrient DWS workflows for document conversion, OCR, data extraction, redaction, watermarking, signing, page manipulation, form filling, and credit checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected documents, form data, redaction targets, and signing inputs may be sent to Nutrient's cloud API for processing.

Mitigation: Use only documents approved for third-party cloud processing, review Nutrient account data-handling policies, and avoid highly sensitive or regulated files unless that processing is approved.

Risk: Runtime setup can rely on an unpinned npm package when the MCP server is launched with npx.

Mitigation: Pin or preinstall a reviewed version of the Nutrient DWS MCP server instead of relying on an unpinned runtime download.

Risk: A broad MCP sandbox path may expose more local files than intended to document-processing tools.

Mitigation: Configure a narrow SANDBOX_PATH that contains only the files needed for the current workflow.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/jdrhyne/skills/nutrient-document-processing-universal)
- [Nutrient Processor API](https://www.nutrient.io/api/)
- [Nutrient DWS Processor guides](https://www.nutrient.io/guides/dws-processor/)
- [Nutrient Processor API playground](https://dashboard.nutrient.io/processor-api/playground/)
- [Nutrient agent skill repository](https://github.com/PSPDFKit-labs/nutrient-agent-skill)
- [Nutrient DWS MCP Server repository](https://github.com/PSPDFKit/nutrient-dws-mcp-server)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration, code]

**Output Format:** [Markdown with JSON configuration examples and bash/curl command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide agents to produce or transform document files through Nutrient cloud API calls using user-selected inputs and configured sandbox paths.]

## Skill Version(s):

1.1.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
