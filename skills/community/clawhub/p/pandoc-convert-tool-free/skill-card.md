## Description: <br>
Pandoc转换工具（免费版） helps agents convert documents between Markdown, HTML, Word, PDF, and related formats using Pandoc-oriented commands and configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, technical writers, and individual users can use this skill to guide single-file document conversion, basic batch conversion, and template-based Pandoc workflows. It is intended for everyday document-format conversion tasks where the user can provide explicit input and output file paths. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local document conversion can run Pandoc commands and create or replace output files. <br>
Mitigation: Use the skill in a specific working folder, name exact input and output paths, and ask for confirmation before overwriting files. <br>
Risk: Batch conversion can affect multiple files at once. <br>
Mitigation: Review the file list and destination directory before running batch conversions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/pandoc-convert-tool-free) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and bash code examples plus JSON or YAML configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create converted document files in the user's working folder when the agent runs Pandoc.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
