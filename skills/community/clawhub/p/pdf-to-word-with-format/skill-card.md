## Description: <br>
Converts PDF documents into editable Word `.docx` files while preserving common formatting such as fonts, sizes, paragraph spacing, alignment, text styling, tables, and images where possible. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yechao1995](https://clawhub.ai/user/yechao1995) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and document-processing teams use this skill to convert PDFs into editable Word documents while retaining common layout and formatting for review or downstream editing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing dependencies into a shared Python environment can affect unrelated projects. <br>
Mitigation: Install the required Python packages in a virtual environment before running the converter. <br>
Risk: Batch conversion or an unintended input path can process more PDFs than intended. <br>
Mitigation: Run the converter only on PDFs or folders selected for the task. <br>
Risk: Generated Word files may be written to an unintended location or overwrite expected outputs. <br>
Mitigation: Choose a dedicated output directory or explicit output filename for each conversion run. <br>


## Reference(s): <br>
- [Format Reference](references/format_reference.md) <br>
- [ClawHub Skill Release](https://clawhub.ai/yechao1995/pdf-to-word-with-format) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, files, guidance] <br>
**Output Format:** [Markdown guidance with bash commands and generated `.docx` files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local Word documents in the selected output path; batch mode writes one `.docx` file per input PDF.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
