## Description:

This skill provides hybrid retrieval (BM25 semantic search + TF-IDF vector similarity) for intelligent template auto-filling. Use when users need to batch fill Word/Excel templates from knowledge bases with high precision matching.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deweienweide](https://clawhub.ai/user/deweienweide)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations users use this skill to batch fill Word and Excel templates from structured JSON knowledge bases when exact field names, similar Chinese field names, and placeholders need to be matched consistently.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated Word or Excel files may contain incorrect values when template fields are ambiguous or the knowledge base uses incompatible field names.

Mitigation: Test on one copied template first and manually review every generated file before submitting or sharing it.

Risk: The bundled scripts read local files and write filled output files using configured paths.

Mitigation: Run the skill in an isolated working directory with copied inputs and review output paths before execution.

Risk: The filler depends on python-docx and openpyxl for document processing.

Mitigation: Pin and verify these dependencies before installation.

Risk: The main script includes hard-coded Windows paths and a hard-coded placeholder replacement value.

Mitigation: Edit the configured knowledge base path, template directory, output directory, and placeholder replacement before running.

## Reference(s):

- [Quick Start Guide](references/quick_start.md)
- [Knowledge Base Format Specification](references/kb_format.md)
- [Algorithm Details](references/algorithms.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance with inline code blocks; bundled Python scripts produce filled .docx and .xlsx files plus console logs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The filler reads a local JSON knowledge base and local template files, then writes filled document or spreadsheet copies to a configured output directory.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
