## Description: <br>
Convert documents between formats using Pandoc, including HTML, Markdown, DOCX, PDF, EPUB, LaTeX, ODT, RST, Org, MediaWiki, JIRA, CSV, and Jupyter notebooks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oliver-hrkltz](https://clawhub.ai/user/oliver-hrkltz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, writers, and technical users use this skill to convert documents across Pandoc-supported formats, apply styling or templates, and generate outputs such as PDF, DOCX, HTML, EPUB, or Markdown. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Untrusted documents or advanced Pandoc options such as filters, templates, resource paths, media extraction, and HTML/CSS PDF engines may load or process unexpected resources. <br>
Mitigation: Use the skill for user-directed conversions, inspect advanced options before running them, and isolate conversions when handling untrusted documents. <br>
Risk: Pandoc and optional PDF engines run as local tools and must be installed separately. <br>
Mitigation: Install Pandoc and PDF engines only from trusted sources, and verify the requested engine is available before conversion. <br>
Risk: Converted documents can lose styling fidelity or omit assets when the selected engine, CSS, template, or resource path does not match the source document. <br>
Mitigation: Review generated files before relying on them, and rerun with explicit engine, CSS, reference document, or resource-path options when needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oliver-hrkltz/pandoc) <br>
- [Skill homepage](https://github.com/hrkltz/pandoc-skill) <br>
- [Pandoc documentation](https://pandoc.org) <br>
- [Pandoc supported formats reference](references/formats.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance with shell command examples; conversions may create document files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Converted outputs depend on the requested input and output formats, local Pandoc installation, and available PDF engines.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
