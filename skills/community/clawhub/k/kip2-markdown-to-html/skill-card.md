## Description:

Convert a Markdown file or raw Markdown string into a polished HTML document.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mutour](https://clawhub.ai/user/mutour)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content authors use this skill to convert Markdown files or raw Markdown strings into styled standalone HTML documents with optional templates, CSS, table of contents, heading numbering, metadata, and embedded assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted Markdown may produce unsafe or misleading HTML when published on a trusted site.

Mitigation: Sanitize the generated HTML or disable raw HTML before publishing converted content from untrusted sources.

Risk: Embedding assets or using broad resource paths may include local referenced files in the generated output.

Mitigation: Review resource paths and embedded assets before sharing or publishing the HTML file.

Risk: The converter depends on Pandoc being installed and available on PATH.

Mitigation: Verify the Pandoc installation before relying on the skill in an agent workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mutour/skills/kip2-markdown-to-html)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance with shell commands and generated standalone HTML files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated HTML can use built-in templates, custom Pandoc templates, custom CSS, optional table of contents, numbered headings, metadata, and embedded assets.]

## Skill Version(s):

0.5.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
