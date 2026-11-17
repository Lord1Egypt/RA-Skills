## Description:

Converts Markdown files into formatted Word documents with support for headings, lists, tables, code blocks, images, math formulas, templates, custom styles, and batch workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runmanfm-bit](https://clawhub.ai/user/runmanfm-bit)

### License/Terms of Use:


## Use Case:

Developers, technical writers, and document authors use this skill to convert Markdown source documents into Word files, including single-file, batch, image-aware, and template-based conversion workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Markdown image references can embed local image files available to the conversion process.

Mitigation: Convert only trusted Markdown or run conversion in a sandbox with access limited to the intended input, image, and output folders; review image references before producing DOCX files.

Risk: Shared temporary-file cleanup is under-scoped.

Mitigation: Run image conversion in an isolated temporary workspace and review cleanup behavior before using the skill on shared systems.

Risk: Dependency installation can affect the host Python environment if run globally.

Mitigation: Install dependencies in a virtual environment and avoid sudo unless system-level packages are deliberately required.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/runmanfm-bit/skills/markdown-to-word-skill)
- [Artifact Skill Documentation](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands that produce DOCX files and optional JSON reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output paths, template selection, image directories, recursive batch processing, and conversion reports are controlled by command-line options.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
