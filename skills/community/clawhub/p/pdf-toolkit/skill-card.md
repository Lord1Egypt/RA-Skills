## Description: <br>
Run a local script to work with PDF files, DOCX documents, OCR, and text-to-speech. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[youpele52](https://clawhub.ai/user/youpele52) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to inspect, extract, merge, split, rotate, create, OCR, and convert PDF or DOCX documents from local command-line workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads from and writes to user-supplied document paths on the host. <br>
Mitigation: Run it only on intended files and review output destinations before execution. <br>
Risk: The text-to-speech command sends input text to an external service. <br>
Mitigation: Avoid using text-to-speech with confidential PDFs, DOCX files, or private text unless external processing is acceptable. <br>


## Reference(s): <br>
- [pypdf Documentation](https://pypdf.readthedocs.io) <br>
- [ClawHub Skill Page](https://clawhub.ai/youpele52/pdf-toolkit) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance] <br>
**Output Format:** [Plain text with labeled sections, command guidance, and generated document or audio files when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Errors are prefixed with "Error:"; the doctor command reports available and missing optional tools.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
