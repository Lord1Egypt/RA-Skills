## Description: <br>
Convert Markdown files to formatted Word documents (.docx). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[frankxpj](https://clawhub.ai/user/frankxpj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and document authors use this skill to convert a specified Markdown file into a formatted Word document, including headings, tables, lists, blockquotes, and basic bold text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The converter reads a user-specified Markdown file and writes a .docx file, which can overwrite an existing output path. <br>
Mitigation: Confirm the exact Markdown input file and intended .docx output path before execution, especially when the output file already exists. <br>
Risk: The skill depends on python-docx when the package is not already installed. <br>
Mitigation: Install python-docx only from a trusted package source. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/frankxpj/md-2-word) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and a generated .docx file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads a local Markdown input path and writes a local .docx output path.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
