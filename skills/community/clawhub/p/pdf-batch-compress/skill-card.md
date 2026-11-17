## Description:

Compresses PDF files above a configurable size threshold using Ghostscript first and PyMuPDF fallback rendering when needed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sereinone](https://clawhub.ai/user/sereinone)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document-processing users can use this skill to batch-compress large PDF collections on macOS or Linux, with configurable size thresholds and parallel execution. It is best suited for workflows where users can review lossy compression results and maintain backups before replacing originals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can overwrite many original PDFs with lossy compressed replacements.

Mitigation: Run it only on copies or with verified backups, and review output quality before applying it to important document sets.

Risk: PyMuPDF fallback may rasterize pages, reducing visual quality, searchability, and accessibility.

Mitigation: Use conservative thresholds when quality matters and inspect representative compressed PDFs before processing a full batch.

Risk: Logs and temporary files are written under shared temporary directories by default.

Mitigation: Use private log and temporary directories before running the skill on sensitive document collections.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sereinone/skills/pdf-batch-compress)
- [Project homepage](https://github.com/weidong/pdf-batch-compress)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May run bundled scripts that emit pipe-delimited compression logs and summary reports.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
