## Description: <br>
Call the IteraTools multi-tool API for 80+ paid agent tools, including image generation, browser automation, web scraping, OCR, document processing, code execution, messaging, productivity, maps, and utility APIs through MCP or REST. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fredpsantos33](https://clawhub.ai/user/fredpsantos33) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent builders use this skill to connect agents to the IteraTools hosted API or MCP server for paid multimodal, web, document, messaging, code, productivity, and utility actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill exposes a broad paid third-party tool suite, including tools that can act on external services. <br>
Mitigation: Enable only the specific IteraTools capabilities needed for the workflow and require confirmation before account-changing or externally visible actions. <br>
Risk: API keys or payment-enabled credentials could create unexpected cost or account exposure. <br>
Mitigation: Use a dedicated low-balance or scoped API key where available and monitor usage. <br>
Risk: Messaging, code execution, browser automation, and provider-side memory tools can process sensitive data or perform high-impact actions. <br>
Mitigation: Avoid sending secrets or sensitive personal data and require human review before these tool categories are invoked. <br>


## Reference(s): <br>
- [IteraTools Homepage](https://iteratools.com) <br>
- [IteraTools Documentation](https://docs.iteratools.com) <br>
- [IteraTools Tools Reference](https://docs.iteratools.com/#tools-reference) <br>
- [IteraTools API](https://api.iteratools.com) <br>
- [IteraTools MCP Server](https://mcp.iteratools.com/mcp) <br>
- [mcp-iteratools on npm](https://www.npmjs.com/package/mcp-iteratools) <br>
- [iteratools-mcp GitHub Repository](https://github.com/fredpsantos33/iteratools-mcp) <br>
- [IteraTools on Smithery](https://smithery.ai/server/iterasoft/iteratools) <br>
- [ClawHub Skill Page](https://clawhub.ai/fredpsantos33/iteratools-api) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, Shell commands, API calls, Code] <br>
**Output Format:** [Markdown with inline shell, JSON, and API configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include instructions for using a paid third-party API key or x402 micropayments.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
