## Description: <br>
Converts Markdown files into high-fidelity PDFs with GitHub-flavored Markdown, code highlighting, tables, task lists, table of contents generation, custom CSS, themes, math, emoji, and optional Mermaid diagrams. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhouchang1988](https://clawhub.ai/user/zhouchang1988) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, technical writers, and document maintainers use this skill to convert Markdown documentation, guides, notes, and reports into PDF files while preserving editor-like rendering, syntax highlighting, page layout, and optional document navigation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan reports that the skill renders user documents in a network-enabled browser with raw HTML support. <br>
Mitigation: Install only when the Markdown source is trusted, or run conversion inside a contained environment without sensitive local files or broad network access. <br>
Risk: Optional Mermaid rendering loads Mermaid from a remote CDN during rendering. <br>
Mitigation: Avoid the --mermaid option unless remote code loading is acceptable, or vendor Mermaid locally before use. <br>
Risk: Raw HTML in Markdown can affect the rendered browser document. <br>
Mitigation: Review or sanitize untrusted Markdown before conversion, especially when custom CSS, embedded HTML, or external resources are present. <br>


## Reference(s): <br>
- [Skill README](README.md) <br>
- [Skill definition](SKILL.md) <br>
- [Renderer script package metadata](scripts/package.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated PDF files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The renderer accepts a Markdown input path, optional PDF output path, theme, CSS, margins, paper size, landscape mode, table of contents, headers, footers, math and emoji toggles, Mermaid rendering, page breaks, and timeout settings.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and scripts/package.json; SKILL.md frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
