## Description: <br>
Edit PDFs with natural-language instructions using the nano-pdf CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kenswj](https://clawhub.ai/user/kenswj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and document authors use this skill to ask an agent to edit a specified PDF page through the nano-pdf command-line tool and then review the resulting PDF. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The external nano-pdf package edits user-provided PDF files, so incorrect commands or tool behavior could change the wrong page or produce inaccurate document output. <br>
Mitigation: Install only when comfortable trusting the external package, keep backups for important PDFs, verify page numbering, and review edited PDFs before sharing or relying on them. <br>


## Reference(s): <br>
- [Nano Pdf release on ClawHub](https://clawhub.ai/kenswj/nano-pdf-1-0-0) <br>
- [nano-pdf package on PyPI](https://pypi.org/project/nano-pdf/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the external nano-pdf CLI and user review of edited PDF output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
