## Description:

Extracts highlighted text annotations from a user-provided PDF and creates a Markdown notes file with YAML front matter, original excerpts grouped by page, and an AI-written summary.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhengbin1973](https://clawhub.ai/user/zhengbin1973)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and developers can use this skill to turn PDF highlight annotations into structured reading notes. It is useful when a user provides a PDF and asks to extract highlights, organize annotations, read marked passages, or generate study notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs PyMuPDF into the active Python environment at runtime.

Mitigation: Run it in an isolated environment and pin or approve the PyMuPDF version before installation.

Risk: The skill writes a highlights Markdown file beside the source PDF and may replace a same-named notes file.

Mitigation: Check whether <pdf name>_highlights.md already exists, or choose a controlled output directory before running it on important documents.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhengbin1973/skills/pdf-highlight-extractor)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [JSON highlight records and a Markdown file with YAML front matter]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Markdown is saved beside the source PDF as <pdf name>_highlights.md; optional color filtering supports yellow, green, red, blue, pink, orange, purple, and cyan.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
