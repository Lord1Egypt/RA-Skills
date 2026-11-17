## Description:

Notebook Builder helps agents create, append, modify, merge, and export Jupyter notebooks with support for embedded local images, table-of-contents cells, tags, and hash-based quiz checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aigamatrix](https://clawhub.ai/user/aigamatrix)

### License/Terms of Use:

MIT

## Use Case:

Developers, educators, and technical writers use this skill to build and maintain teaching notebooks, programming exercises, technical tutorials, and study notes in manageable segments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Quiz text, hints, or question IDs from untrusted sources can be inserted into executable Python notebook cells.

Mitigation: Review generated notebooks before running quiz cells, and use trusted quiz inputs for assessed exercises.

Risk: Ambiguous output paths can create or modify unintended project files.

Mitigation: Specify target notebook and export paths clearly before running helper commands.

Risk: The local hash quiz system is visible in the notebook and is not suitable for secure exams or certification grading.

Mitigation: Use it for teaching and formative checks only; use a secure external assessment system for high-stakes grading.

## Reference(s):

- [Artifact README](artifact/README.md)
- [ClawHub skill page](https://clawhub.ai/aigamatrix/skills/notebook-builder)

## Skill Output:

**Output Type(s):** [markdown, code, shell commands, files, guidance]

**Output Format:** [Markdown guidance with Python helper calls and generated .ipynb or .py files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May embed local image data as base64 and write notebook files to user-specified paths.]

## Skill Version(s):

1.0.3 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
