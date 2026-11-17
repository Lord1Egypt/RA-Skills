## Description:

PDF splitting and PDF-to-Word conversion tools implemented in Node.js.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daguniang](https://clawhub.ai/user/daguniang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to split selected PDF page ranges into new PDFs or convert PDF text into simple .docx files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads source PDFs and writes output files on local paths, so an incorrect output path could overwrite important files.

Mitigation: Use explicit output paths in a workspace directory and avoid writing over important existing files.

Risk: The supplied security guidance notes a vulnerable transitive nanoid dependency in the npm dependency set.

Mitigation: Review, update, or pin dependencies before use.

## Reference(s):


## Skill Output:

**Output Type(s):** [Files, Text, Shell commands, Guidance]

**Output Format:** [PDF and DOCX files with status text or JSON-like status objects]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [PDF-to-Word conversion extracts text into a simple DOCX and does not preserve complex PDF layout.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
