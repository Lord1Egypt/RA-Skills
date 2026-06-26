## Description: <br>
Converts Markdown files into styled PDF documents with Chinese text support, code highlighting, tables, links, images, and WeasyPrint-based CSS rendering. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[franklu0819-lang](https://clawhub.ai/user/franklu0819-lang) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, technical writers, and teams use this skill to convert Markdown documentation into polished PDF files, especially when Chinese text, tables, code blocks, links, and images need consistent rendering. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may automatically install Python packages and system fonts on the host when dependencies are missing. <br>
Mitigation: Review the pip and yum commands before running the wrapper script, prefer a virtual environment or container, and avoid elevated privileges unless system-level font installation is intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/franklu0819-lang/md2pdf-weasyprint) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and generated PDF files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The conversion scripts read a Markdown input file and write a PDF output file.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
