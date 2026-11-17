## Description:

Convert Markdown files to styled PDFs using pandoc and wkhtmltopdf with built-in or custom CSS style options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mengwuzhi](https://clawhub.ai/user/mengwuzhi)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to convert Markdown documents into consistently styled PDF files with selectable built-in CSS styles or a trusted custom CSS file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The renderer is given broad local file access, which could expose local files when converting untrusted Markdown or CSS.

Mitigation: Convert only trusted Markdown and CSS, or run the skill in a sandboxed, low-privilege environment with local file access restricted or removed.

Risk: Conversion depends on local pandoc and wkhtmltopdf installations.

Mitigation: Verify both tools are installed and available before using the skill in a workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mengwuzhi/skills/markdown-to-pdf-styled)
- [Usage guide](references/usage.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with bash command examples and generated PDF file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces PDF files from Markdown using clean, modern, paper, or trusted custom CSS styles.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill documentation)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
