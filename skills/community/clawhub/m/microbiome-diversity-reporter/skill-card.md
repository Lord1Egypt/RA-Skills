## Description:

Interpret Alpha and Beta diversity metrics from 16S rRNA sequencing results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and researchers use this skill to run a bounded workflow for interpreting alpha and beta diversity metrics from 16S rRNA OTU or ASV tables and optional sample metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML can include unescaped sample names or other input-derived fields from OTU/ASV and metadata files.

Mitigation: Use trusted inputs or sanitize and escape sample names before opening or sharing HTML reports.

Risk: Dependency and file boundaries are under-scoped for a local analysis script.

Mitigation: Install in an isolated Python environment, review or pin dependencies, and keep input and output paths inside the workspace.

## Reference(s):

- [Audit Reference](references/audit-reference.md)
- [ClawHub Skill Page](https://clawhub.ai/aipoch-ai/skills/microbiome-diversity-reporter)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, HTML, shell commands, guidance]

**Output Format:** [Markdown, JSON, or HTML reports with command-line execution guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads TSV OTU/ASV tables and optional sample metadata; writes reports to stdout or a specified workspace file.]

## Skill Version(s):

1.0.0 (source: release evidence and script header)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
