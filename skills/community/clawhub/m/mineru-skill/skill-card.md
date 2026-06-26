## Description: <br>
MinerU PDF Parser converts PDF, Office, HTML, and image documents into clean Markdown, JSON status, optional chunks, and export files for agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tsekaluk](https://clawhub.ai/user/tsekaluk) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, analysts, and agent users use this skill to parse local files or URLs into Markdown, run OCR on scanned documents, batch-process folders, and send parsed content to configured knowledge or productivity tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Document contents may be sent to MinerU cloud services or to configured third-party sinks. <br>
Mitigation: Use only approved documents and destinations; avoid confidential or regulated files unless the relevant services are approved by the organization. <br>
Risk: The skill can use OAuth tokens and sensitive API credentials for MinerU and delivery sinks. <br>
Mitigation: Scope credentials narrowly, store them in an approved secret mechanism, and rotate or revoke tokens that are no longer needed. <br>
Risk: Generated Markdown can contain local image paths, and some export paths may include or expose referenced local files. <br>
Mitigation: Review generated Markdown and assets before exporting to third-party tools, especially when using Linear or other sinks that process local image references. <br>


## Reference(s): <br>
- [MinerU Skill page](https://clawhub.ai/tsekaluk/mineru-skill) <br>
- [MinerU homepage](https://mineru.net) <br>
- [MinerU API docs](https://mineru.net/apiManage/docs) <br>
- [MinerU token management](https://mineru.net/apiManage/token) <br>
- [MinerU API Reference](references/api_reference.md) <br>
- [Delivery Integrations](references/integrations.md) <br>
- [Competitive Comparison Reference](references/comparison.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown files or stdout, JSON status and chunk sidecars, optional DOCX/HTML/LaTeX exports, and sink delivery results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local output directories with extracted images and may deliver Markdown to configured third-party sinks.] <br>

## Skill Version(s): <br>
3.3.1 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
