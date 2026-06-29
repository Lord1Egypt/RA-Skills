## Description: <br>
md2pdf helps an agent convert Markdown documents into polished PDFs with covers, tables of contents, bookmarks, page numbers, KaTeX, Mermaid diagrams, syntax highlighting, and themed layout options. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codermoray](https://clawhub.ai/user/codermoray) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, writers, and documentation teams use this skill to turn Markdown reports, technical notes, and other documents into PDF files through an agent-guided workflow. The skill is useful when users want configurable covers, tables of contents, themes, Chinese layout support, math, diagrams, and code highlighting without manually assembling conversion commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may install or require large rendering dependencies such as pandoc, Playwright, and Chromium. <br>
Mitigation: Review dependency size and installation source before deployment, especially in managed or bandwidth-limited environments. <br>
Risk: First-run rendering may download JavaScript assets for Mermaid diagrams or syntax highlighting. <br>
Mitigation: For sensitive or offline environments, confirm asset sources and prefer pinned or vendored copies before use. <br>
Risk: PDF password settings could expose sensitive values if stored in shared configuration defaults. <br>
Mitigation: Keep encryption disabled by default and avoid storing important PDF passwords in reusable configuration files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/codermoray/skills/md2pdf) <br>
- [Publisher profile](https://clawhub.ai/user/codermoray) <br>
- [Project homepage](https://github.com/CoderMoray/md2pdf) <br>
- [README](README.md) <br>
- [Skill definition](SKILL.md) <br>
- [Theme development guide](themes/DEVELOPMENT.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration examples; successful runs produce PDF files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports theme, page size, font, cover, table of contents, KaTeX, Mermaid, syntax highlighting, header, watermark, and optional password settings.] <br>

## Skill Version(s): <br>
1.7.0 (source: SKILL.md frontmatter and ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
