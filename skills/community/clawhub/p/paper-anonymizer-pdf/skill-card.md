## Description:

Comprehensive PDF manipulation toolkit for extracting text and tables, creating new PDFs, merging/splitting documents, and handling forms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lnj22](https://clawhub.ai/user/lnj22)

### License/Terms of Use:

Proprietary

## Use Case:

Developers and agents use this skill to process PDFs locally, including extracting content, creating or modifying documents, merging or splitting files, and completing PDF forms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PDF processing can expose sensitive document contents through temporary files such as form JSON, rendered page images, extracted text, or generated PDFs.

Mitigation: Process only authorized documents, choose output paths deliberately, and delete temporary JSON, image, and extracted-content files when they contain sensitive data.

Risk: PDF modification, repair, password, merge, split, or form-fill operations can overwrite files or create incorrect documents if inputs or paths are wrong.

Mitigation: Keep backups before destructive or in-place workflows, review generated commands before execution, and verify output PDFs before using or sharing them.

Risk: Putting real passwords directly on command lines can expose credentials through shell history or process inspection.

Mitigation: Avoid command-line password literals when possible and prefer safer secret handling supported by the chosen PDF tool.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lnj22/skills/paper-anonymizer-pdf)
- [PDF form workflow](artifact/forms.md)
- [PDF processing advanced reference](artifact/reference.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python, JavaScript, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local PDF files, extracted text, table data, images, form field JSON, or filled documents when the agent follows the guidance.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
