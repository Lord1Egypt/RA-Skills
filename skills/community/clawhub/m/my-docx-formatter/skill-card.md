## Description: <br>
Generates Word documents in Chinese official-document style from Markdown or JSON input, including headings, fonts, paragraph formatting, page numbers, and Chinese punctuation handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liujiang817](https://clawhub.ai/user/liujiang817) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to create formatted .docx files for formal Chinese documents such as reports, summaries, plans, and official materials from Markdown or structured JSON content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad activation wording may cause the formatter to run for general document requests. <br>
Mitigation: Confirm the user wants Chinese official-document-style Word output and use explicit input and output paths before running the formatter. <br>
Risk: The install script installs python-docx into a local virtual environment. <br>
Mitigation: Review the install script before first use and run it only in the intended skill directory. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liujiang817/my-docx-formatter) <br>
- [Publisher profile](https://clawhub.ai/user/liujiang817) <br>


## Skill Output: <br>
**Output Type(s):** [files, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands that produce .docx files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local input and output paths; generated documents are saved as .docx files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
