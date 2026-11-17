## Description: <br>
文档导出工具免费版 helps content creators and developers convert local Markdown files into DOCX, PDF, HTML, spreadsheet, structured data, and related document formats through a command-line workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, content creators, and developers use this skill to install and run a local Markdown export CLI for converting Markdown documents, tables, and code blocks into deliverable document, web, spreadsheet, data, and extracted-code files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can write converted output files and may overwrite important files if an output path is chosen carelessly. <br>
Mitigation: Use explicit input and output paths, and avoid pointing outputs at important existing files unless replacement is intended. <br>
Risk: The artifact contains broad CRUD and network troubleshooting language that is not central to Markdown conversion. <br>
Mitigation: Treat that language as documentation noise and limit agent actions to local Markdown export tasks. <br>
Risk: The workflow depends on local command execution and an installed Markdown export CLI. <br>
Mitigation: Install only in environments where local command execution is acceptable, then verify commands and generated files before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/md-export-tool-free) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text] <br>
**Output Format:** [Markdown guidance with bash command examples and JSON-style status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses explicit local input and output file paths; converted output files are written by the local export CLI.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
