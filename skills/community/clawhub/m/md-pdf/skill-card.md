## Description:

Converts Markdown to polished PDF through either a Pandoc and XeLaTeX print pipeline or a browser-rendered HTML and Twemoji pipeline for emoji-heavy output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[karlzhu-zxc](https://clawhub.ai/user/karlzhu-zxc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical writers use this skill to turn Markdown documents into print-ready PDFs, including CJK-friendly reports and emoji-heavy documents that need browser-style rendering.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser-based rendering can expose sensitive Markdown content to an existing or remote browser session.

Mitigation: Use the browser pipeline only with a trusted local or access-controlled CDP endpoint and avoid processing sensitive or untrusted Markdown through it.

Risk: Active Markdown or embedded HTML may execute during browser rendering.

Mitigation: Add sanitization, disable JavaScript where possible, and block unnecessary network requests before routine use.

Risk: The browser pipeline installs npm dependencies without a lockfile.

Mitigation: Pin dependencies with a lockfile before adopting the skill in a repeatable production workflow.

## Reference(s):

- [md2pdf style guide](references/style-guide.md)
- [Reusable defaults preset](assets/defaults/hifi.yaml)
- [ClawHub skill page](https://clawhub.ai/karlzhu-zxc/skills/md-pdf)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces guidance for generating PDF files from Markdown using local command-line tools.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
