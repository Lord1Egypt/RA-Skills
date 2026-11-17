## Description:

HTML-first PDF production skill for reports, papers, and structured documents. Must be applied before generating PDF deliverables from HTML.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krisliu16](https://clawhub.ai/user/krisliu16)

### License/Terms of Use:


## Use Case:

Developers and document-producing agents use this skill to author and convert HTML into print-quality PDFs with stable pagination, searchable text, preserved links, citation integrity, and predictable layout.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill strongly steers agents toward a specific HTML-to-PDF workflow, so misuse on unrelated PDF tasks could produce the wrong handling path.

Mitigation: Classify the request intent first and use the existing-PDF, LaTeX, build, or transform path that matches the user task.

Risk: Minor ambiguity in CSS counter guidance or print CSS choices could lead to layout, numbering, or pagination defects.

Mitigation: Review generated HTML and CSS, use explicit labels for figures, tables, and equations, and run the hyperlink, image, anchor, and structure fidelity gates before delivery.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with HTML, CSS, and command-oriented instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Steers agents toward the html_to_pdf conversion pipeline and print-oriented fidelity checks.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
