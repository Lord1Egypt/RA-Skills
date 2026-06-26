## Description: <br>
Edit PDFs with natural-language instructions using the nano-pdf CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[utromaya-code](https://clawhub.ai/user/utromaya-code) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, document editors, and other external users use this skill to edit a target PDF page by giving the nano-pdf CLI a natural-language instruction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs and invokes the third-party nano-pdf CLI and its AI service dependencies. <br>
Mitigation: Install only if you trust the nano-pdf package and use it on PDFs you are comfortable processing through that tool. <br>
Risk: PDF edits may be incorrect, including edits to the wrong page if page numbering differs by tool version or configuration. <br>
Mitigation: Keep backups, check whether the page index is 0-based or 1-based, and review the edited PDF before sharing it. <br>


## Reference(s): <br>
- [Nano Pdf on ClawHub](https://clawhub.ai/utromaya-code/nano-pdf-editor) <br>
- [nano-pdf PyPI project](https://pypi.org/project/nano-pdf/) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, guidance, files] <br>
**Output Format:** [Markdown with inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The nano-pdf CLI edits PDF files; users should review output PDFs before sharing.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
