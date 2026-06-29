## Description: <br>
MarkItDown Hosted Markdown Generator converts files and URLs into Markdown through AgentPMT-hosted remote tool calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentpmt](https://clawhub.ai/user/agentpmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to convert PDFs, Office documents, spreadsheets, presentations, HTML pages, CSV, JSON, XML, images, audio, EPUB files, ZIP archives, or URLs into Markdown for analysis, indexing, summarization, and downstream workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Hosted document conversion can expose submitted documents, URLs, or file contents to the third-party service provider. <br>
Mitigation: Submit only content you are authorized to process with AgentPMT, and avoid secrets, regulated data, private business documents, and internal signed URLs unless the provider is approved for that data. <br>
Risk: Incorrect input selection or stale schema details can cause failed conversions or unintended document handling. <br>
Mitigation: Use exactly one supported input method per request and fetch live schema or instructions before production integrations when parameters, outputs, or examples are unclear. <br>


## Reference(s): <br>
- [AgentPMT MarkItDown marketplace](https://www.agentpmt.com/marketplace/markitdown) <br>
- [ClawHub skill page](https://clawhub.ai/agentpmt/skills/markitdown-hosted-markdown-generator) <br>
- [Generated action schema](artifact/schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, JSON] <br>
**Output Format:** [JSON response containing converted Markdown text and metadata] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns the action name, input source, converted Markdown, and Markdown character length; individual inputs are limited to 50 MB.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
