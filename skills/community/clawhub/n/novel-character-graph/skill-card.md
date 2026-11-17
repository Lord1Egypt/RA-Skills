## Description:

Analyzes long-form novels, maps characters and relationships, prepares worldview and timeline outputs, builds interactive HTML relationship graphs, and drafts theme-song prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mengbin92](https://clawhub.ai/user/mengbin92)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, writers, and content teams use this skill to analyze novels in TXT, EPUB, PDF, DOCX, or MOBI form and produce character systems, relationship maps, timelines, worldview notes, interactive graph reports, and song-generation prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports that the skill explicitly allows dependency installation without user approval.

Mitigation: Require explicit user approval before any apt, sudo, pip, media conversion, or package-installation command is run.

Risk: Generated HTML reports can expose users to unsafe content if untrusted novel data is inserted without escaping or if remote scripts are loaded.

Mitigation: Open generated reports only after reviewing the template and escaping behavior, and avoid remote script loading for untrusted inputs.

Risk: Preprocessing and conversion commands can overwrite or transform source novel files.

Mitigation: Keep backups of source novels and write converted files, split chapters, Markdown reports, and HTML outputs to a separate working directory.

## Reference(s):

- [Format Handbook](references/format_handbook.md)
- [ClawHub Skill Page](https://clawhub.ai/mengbin92/skills/novel-character-graph)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown, shell commands, Python-generated HTML, and Suno-style song prompt text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can create novel analysis Markdown files and an interactive HTML relationship graph; users should review commands and generated HTML before use.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
