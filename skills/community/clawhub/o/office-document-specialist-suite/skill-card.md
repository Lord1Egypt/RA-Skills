## Description:

Creates Word .docx report templates and applies document styling through a local Python CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[robert-janssen](https://clawhub.ai/user/robert-janssen)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to generate basic Word report templates and apply consistent formatting to existing .docx documents. It is best suited for local document preparation workflows rather than full Office automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The public skill description claims Word, Excel, and PowerPoint support, while the artifact implementation only provides Word .docx template and styling commands.

Mitigation: Use the skill for .docx workflows unless additional spreadsheet or presentation tooling is verified separately.

Risk: Setup installs Python dependencies for local document generation.

Mitigation: Review and pin dependencies before use in sensitive or controlled environments.

Risk: Generated document text defaults to Dutch.

Mitigation: Review and localize generated content before sharing documents externally.

## Reference(s):


## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [Word .docx files plus Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated document template text defaults to Dutch.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
