## Description:

Batch process local PDF files by merging documents, splitting pages or ranges, rotating pages, and extracting text with command-line Python scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[potatosolo](https://clawhub.ai/user/potatosolo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operations staff, and other document-heavy users use this skill to automate local PDF workflows without uploading files to an external service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned Python dependency ranges can install newer dependency versions with changed behavior or vulnerabilities.

Mitigation: Install in an isolated environment and pin reviewed versions of dependencies before using the skill with important or untrusted PDFs.

Risk: The skill text mentions image extraction and PDF compression, but the artifact only includes merge, split, rotate, and text extraction scripts.

Mitigation: Use only the implemented workflows unless image extraction or compression scripts are added and reviewed.

Risk: Processing untrusted PDFs may expose the local environment to parser bugs in PDF libraries.

Mitigation: Process untrusted PDFs in a sandboxed or disposable environment and keep dependency versions reviewed and patched.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/potatosolo/skills/pdf-batch-processing-tool)
- [Publisher Profile](https://clawhub.ai/user/potatosolo)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with command examples and generated local PDF or text files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs local Python scripts for merge, split, rotate, and text extraction workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
