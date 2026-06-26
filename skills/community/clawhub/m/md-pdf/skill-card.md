## Description: <br>
Convert Markdown to polished PDF using Pandoc and XeLaTeX for print-quality documents or browser rendering with emoji and CSS support for rich visuals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[karlzhu-zxc](https://clawhub.ai/user/karlzhu-zxc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to convert Markdown files into polished PDFs, choosing either a formal Pandoc/XeLaTeX pipeline or an emoji-friendly browser-rendered pipeline. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The browser-based PDF path can send Markdown document content to a configured CDP browser endpoint. <br>
Mitigation: Use the Pandoc/XeLaTeX path for untrusted or private files, and only use a trusted local CDP browser for browser rendering. <br>
Risk: The browser pipeline may install npm dependencies automatically on first use. <br>
Mitigation: Review dependency installation in the target environment before running the browser pipeline. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/karlzhu-zxc/md-pdf) <br>
- [md2pdf style guide](references/style-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and configuration file references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local PDF files through Pandoc/XeLaTeX or an existing CDP browser endpoint.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
