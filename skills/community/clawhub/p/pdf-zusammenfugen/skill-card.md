## Description:

PDF Zusammenfügen helps German-language users merge local PDF files in a chosen order, including structured application PDFs with privacy-aware checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wsgtcyx](https://clawhub.ai/user/wsgtcyx)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to combine multiple local PDF files in a defined order, especially German application packages, while confirming paths, overwrite behavior, and result readability.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The merged PDF can be incorrect if the user supplies files in the wrong order or chooses the wrong output path.

Mitigation: Confirm the input order, output path, and overwrite choice before running the merge.

Risk: Dependency installation can reduce reproducibility if packages are installed ad hoc.

Mitigation: Prefer installing pypdf in a virtual environment or from a pinned, trusted requirements file.

Risk: Encrypted PDFs may fail to merge when they cannot be opened without a password.

Mitigation: Check whether inputs are password protected before running the merge and request usable files when needed.

## Reference(s):

- [PDF zusammenfügen](https://pdfzus.de/)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Files]

**Output Format:** [Markdown guidance with bash commands and local PDF file output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local PDF inputs and a Python PDF backend such as pypdf or PyPDF2.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
