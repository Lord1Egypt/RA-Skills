## Description:

Convert documents between formats using Pandoc CLI, including Markdown, DOCX, PDF, HTML, EPUB, PPTX, ODT, RTF, LaTeX, CSV/TSV, and Jupyter.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tridefender](https://clawhub.ai/user/tridefender)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, technical writers, and operations teams use this skill to ask an agent for Pandoc commands, configuration, and workflow guidance for converting, extracting, and formatting documents across common publishing formats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Advanced Pandoc options can turn document conversion into local command execution or unsafe file access when used on untrusted documents.

Mitigation: Require explicit approval for advanced options and avoid shell escape, executable filters, Lua scripts, remote URLs, and server mode unless the conversion runs in a tightly scoped sandbox with limited files, no secrets, and controlled network access.

## Reference(s):

- [Pandoc Advanced Reference](references/advanced.md)
- [ClawHub skill page](https://clawhub.ai/tridefender/skills/pandoc-convert)
- [Publisher profile](https://clawhub.ai/user/tridefender)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May lead an agent to produce converted document files when the proposed Pandoc commands are executed.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
