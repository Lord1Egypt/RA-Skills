## Description:

Use when a task needs a local Markdown file path or pasted Markdown text converted into a faithful mobile-friendly PNG/JPG long image for phone-readable articles, guides, notes, or reports, with HTML kept beside the image for inspection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linsuisheng034](https://clawhub.ai/user/linsuisheng034)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content authors use this skill to convert local Markdown files or pasted Markdown into phone-readable long-form PNG/JPG images while retaining an HTML sidecar for inspection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may modify the Python environment by installing required packages or browser components.

Mitigation: Run it in an isolated environment and preinstall expected dependencies where possible.

Risk: Untrusted Markdown can include raw HTML or remote content that is rendered in Chromium.

Mitigation: Avoid untrusted Markdown or disable raw HTML and remote network requests before processing.

## Reference(s):

- [Workflow](references/workflow.md)
- [Troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash command examples; script output is JSON with generated Markdown, HTML, and image file paths.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces PNG or JPG long images and retains an HTML sidecar on disk.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
