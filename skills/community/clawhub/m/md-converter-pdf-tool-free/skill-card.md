## Description: <br>
Converts Markdown documents to PDF with support for custom styling, headers and footers, tables of contents, and single-file or batch conversion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to convert Markdown files into PDFs for personal documentation workflows, including styled output, tables of contents, and batch conversion when supported by the local environment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent may read local Markdown files and related assets during conversion. <br>
Mitigation: Use explicit input paths and avoid sensitive directories unless those files are intended for conversion. <br>
Risk: The workflow may run local conversion tools such as pandoc and xelatex. <br>
Mitigation: Review the proposed command, input files, and output path before execution. <br>
Risk: Generated PDFs may overwrite existing files if output paths are reused. <br>
Mitigation: Confirm before overwriting and choose a distinct output path for important files. <br>
Risk: Some broad modify/delete language appears to be boilerplate rather than supported skill behavior. <br>
Mitigation: Treat the supported behavior as Markdown-to-PDF conversion unless the release evidence explicitly documents additional file operations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/md-converter-pdf-tool-free) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command and code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide the agent to read Markdown inputs, run pandoc or xelatex, and write PDF output files when paths are explicit.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
