## Description: <br>
Converts Markdown documents into professionally formatted Word documents using configurable presets for Chinese-language document typography. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cat-xierluo](https://clawhub.ai/user/cat-xierluo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, legal professionals, and document authors use this skill to convert Markdown source files into styled Word documents for formal reports, academic papers, legal documents, and service plans. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Markdown image URLs can cause outbound requests to external servers during document conversion. <br>
Mitigation: Run the converter only on trusted Markdown or in a network-restricted environment when processing sensitive content. <br>
Risk: Mermaid diagrams may be rendered through a local executable selected by configuration. <br>
Mitigation: Set MMDCCMD only to a trusted Mermaid CLI binary and avoid untrusted renderer paths. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/cat-xierluo/md2word) <br>
- [Project Homepage](https://github.com/cat-xierluo/legal-skills) <br>
- [Configuration Reference](references/config-reference.md) <br>
- [Usage Examples](references/examples.md) <br>
- [Style Mappings](references/style-mappings.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with Python shell commands, YAML configuration, and generated DOCX files when the conversion scripts run.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports built-in YAML presets, custom configuration files, optional Word templates, tables, images, and optional Mermaid diagram rendering.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
