## Description:

Formats Chinese or English academic papers from supported Word or LaTeX sources, applying thesis, journal, coursework, or user/institution templates while preserving manuscript content and rejecting unsupported inputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cryptocxf](https://clawhub.ai/user/cryptocxf)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to format supplied academic manuscripts into editable Word or LaTeX deliverables while preserving existing text, figures, formulas, and citation relationships. It is suited for thesis, journal, coursework, and similar paper-formatting workflows where an official template or default formatting rules must be applied.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill locally reads and rewrites supplied Word or LaTeX manuscript files.

Mitigation: Use it only for intended academic paper-formatting workflows and review the generated manuscript before submission.

Risk: Default Chinese/GB formatting choices or an auto-filled thesis cover date may not match a user's institution or journal.

Mitigation: Provide official templates when available and explicitly confirm or override missing thesis cover dates.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cryptocxf/skills/paper-format)
- [Word paper formatting guide](artifact/references/word-formatting.md)
- [Graduation thesis formatting guide](artifact/references/graduation-thesis.md)
- [Academic paper formatting guide](artifact/references/academic-paper.md)
- [GB/T 7714-2025 reference rules](artifact/references/gbt7714-2025.md)
- [LaTeX paper templates](artifact/references/templates.md)

## Skill Output:

**Output Type(s):** [Files, Markdown, Shell commands, Guidance]

**Output Format:** [Editable .docx or .tex manuscript file plus concise Markdown validation summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Only the final manuscript is delivered; scripts, logs, intermediate documents, and temporary files are not attached.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
