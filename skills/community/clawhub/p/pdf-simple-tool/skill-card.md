## Description: <br>
PDF splitting and PDF-to-Word conversion tools implemented in Node.js. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daguniang](https://clawhub.ai/user/daguniang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to split selected page ranges from PDFs and convert PDF text into simple Word documents through local Node.js utilities. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local PDFs and writes generated files to user-selected paths, so an existing output file could be overwritten. <br>
Mitigation: Confirm the input PDF, output folder, output filename, and page range before running the tool. <br>
Risk: The skill depends on local npm packages for PDF parsing, PDF manipulation, and DOCX generation. <br>
Mitigation: Install only after reviewing the listed npm dependencies and running the skill in an environment appropriate for local document processing. <br>


## Reference(s): <br>
- [PDF Simple Tool on ClawHub](https://clawhub.ai/daguniang/pdf-simple-tool) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Node.js function calls and local PDF or DOCX file outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads a user-selected PDF path and writes a user-selected PDF or DOCX output path.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
