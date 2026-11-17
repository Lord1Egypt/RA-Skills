## Description:

Convert a Markdown file or raw Markdown string into polished DOCX or HTML output from one unified skill.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mutour](https://clawhub.ai/user/mutour)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, technical writers, and content teams use this skill to export one Markdown source into Word DOCX, HTML, or both while applying built-in or custom publication templates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML from untrusted Markdown may contain active or unsafe content.

Mitigation: Use trusted Markdown for HTML exports, or sanitize and review generated HTML before publishing it or opening it under a trusted origin.

Risk: Custom templates, CSS, resource paths, and output paths are user-controlled inputs to the conversion workflow.

Mitigation: Use trusted local templates and styles, review resource paths before conversion, and choose output locations intentionally.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mutour/skills/markdown-export)
- [Skill Definition](SKILL.md)
- [HTML Export Example](assets/examples/sample-html.md)
- [DOCX Export Example](assets/examples/sample-docx.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with shell commands that produce DOCX or HTML files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires pandoc on PATH; custom templates, CSS, resource paths, Markdown input, and output paths are user-controlled.]

## Skill Version(s):

0.5.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
