## Description:

Assemble 6 sub-figures (A-F) into a high-resolution composite figure with consistent labels, padding, and publication-ready DPI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, authors, and developers use this skill to combine exactly six existing image panels into a labeled 2x3 or 3x2 composite figure for publication workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release security summary says the dependency list is unsafe.

Mitigation: Review dependencies before installation, remove the obsolete pil entry, and pin reviewed versions of Pillow and numpy.

Risk: The release security summary says the script does not enforce the workspace path limits documented by the skill.

Mitigation: Run the skill in an isolated environment and use only trusted image paths until workspace-boundary checks are enforced in code.

Risk: The release security verdict is suspicious even though no specific risk findings were listed.

Mitigation: Review the skill before installing or running it, following the server-provided security guidance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aipoch-ai/skills/multi-panel-figure-assembler)

## Skill Output:

**Output Type(s):** [Files, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown instructions and command examples; execution produces PNG, JPG, or TIFF composite image files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires exactly 6 input image paths and one output path; supports 2x3 and 3x2 layouts, DPI, labels, padding, borders, and colors.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
