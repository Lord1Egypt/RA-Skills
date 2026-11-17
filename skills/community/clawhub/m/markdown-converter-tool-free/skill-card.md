## Description: <br>
Markdown转换器免费版 helps agents convert PDF, Word, Excel, PowerPoint, HTML, image, and data files into Markdown while preserving basic document structure and supporting basic OCR. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, knowledge workers, and agent operators use this skill to convert individual documents and common data formats into Markdown for editing, archiving, and knowledge management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks an agent to execute uvx/markitdown against user-selected files, which can create or overwrite output files if paths are chosen incorrectly. <br>
Mitigation: Review the exact input and output paths before running conversion commands, and use a scratch directory for untrusted or experimental conversions. <br>
Risk: Optional Azure document-intelligence and plugin flags can send document content to external providers or run third-party extensions. <br>
Mitigation: Avoid the -d, -e, and --use-plugins options for confidential documents unless the provider, plugin behavior, and data-handling terms have been reviewed. <br>
Risk: Broad activation wording could cause the skill to be used on sensitive files without enough scoping. <br>
Mitigation: Confirm that the selected files are intended for conversion and that any sensitive content is approved for the chosen local or external processing path. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/markdown-converter-tool-free) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and conversion guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces converted Markdown files or Markdown text from selected input documents; optional OCR, cloud document-intelligence, and plugin behavior depends on the agent environment and selected command options.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
