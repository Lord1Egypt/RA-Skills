## Description: <br>
Batch process PDF files locally, including merge, split, page rotation, and text extraction workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[potatosolo](https://clawhub.ai/user/potatosolo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, automation engineers, and document operations users can use this skill to run local command-line PDF processing for repeated merge, split, rotate, and text extraction tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PDFs from untrusted sources can carry parser and resource-exhaustion risk during local processing. <br>
Mitigation: Use an isolated Python environment, keep dependencies patched, and apply sandboxing or resource limits for untrusted PDFs. <br>
Risk: The release advertises image extraction and compression, but the artifact does not include matching scripts for those workflows. <br>
Mitigation: Rely on the implemented merge, split, rotate, and text extraction scripts until the publisher adds supported image extraction and compression tooling. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/potatosolo/pdf-batch-processing-tool) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and generated local files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local PDF and text files may be written by the provided scripts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
