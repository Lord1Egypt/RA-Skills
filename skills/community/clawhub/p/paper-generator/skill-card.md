## Description:

Generates a starter academic paper Markdown file in English or Chinese from a selected template.

This skill is ready for commercial/non-commercial use.

## Publisher:

[laojun509](https://clawhub.ai/user/laojun509)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and researchers can use this skill to create a first-pass academic paper scaffold from experiment work, with sections such as abstract, introduction, methods, experiments, discussion, conclusion, and references.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documentation describes complete paper generation and PDF conversion, but inspected files only create a basic Markdown outline and do not include the documented PDF conversion command.

Mitigation: Review generated drafts before use and provide a separate, trusted PDF conversion workflow when PDF output is required.

Risk: The skill writes to a user-specified output path.

Mitigation: Run it in a controlled workspace and choose explicit output paths that do not overwrite important files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/laojun509/skills/paper-generator)

## Skill Output:

**Output Type(s):** [markdown, shell commands, guidance]

**Output Format:** [Markdown file plus command-line status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports icml, neurips, and arxiv template choices; supports English and Chinese output.]

## Skill Version(s):

0.1.0 (source: evidence.json release metadata and artifact/SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
