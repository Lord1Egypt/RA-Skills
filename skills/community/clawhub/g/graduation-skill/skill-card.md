## Description:

Graduation Skill guides software technology graduation projects from requirements analysis and system design through prototype creation, document generation, Word formatting, diagram standards, and final submission checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zouboy](https://clawhub.ai/user/zouboy)

### License/Terms of Use:

MIT-0

## Use Case:

Students and developers working on software technology graduation projects use the skill to plan requirements, design system diagrams and prototypes, generate PDF prototype artifacts, standardize Word document formatting, and check final submission details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Word formatting script writes DOCX output to a user-supplied or derived path.

Mitigation: Review input and output paths and keep a backup before running the script.

Risk: The skill depends on pip packages for document and PDF generation.

Mitigation: Use a virtual environment and review or pin python-docx and reportlab before installation.

Risk: The PDF prototype script references a Windows-specific Chinese font path.

Mitigation: Confirm the font exists locally or adjust the font registration path for the target environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zouboy/skills/graduation-skill)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline Python and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local PDF and DOCX files when bundled scripts are run.]

## Skill Version(s):

1.0.0 (source: server release and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
