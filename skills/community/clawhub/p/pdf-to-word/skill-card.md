## Description: <br>
Converts PDF files into editable Word documents in .docx format. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhao1263445468](https://clawhub.ai/user/zhao1263445468) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to convert uploaded or local PDF files into editable Word .docx documents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes user-selected PDF files and writes a .docx file to the chosen or default output path. <br>
Mitigation: Only run it on PDFs intended for conversion and verify the output path before execution. <br>
Risk: The conversion depends on the pinned third-party pdf2docx package. <br>
Mitigation: Review and manage the pinned dependency using the same dependency-scanning process used for other third-party packages. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Files, Text] <br>
**Output Format:** [DOCX file with status text containing the output path] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates a .docx file at the requested output path, or next to the input PDF when no output path is supplied.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
