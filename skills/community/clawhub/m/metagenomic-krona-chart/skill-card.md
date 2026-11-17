## Description:

Analyze data with `metagenomic-krona-chart` using a reproducible workflow, explicit validation, and structured outputs for review-ready interpretation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT

## Use Case:

Developers, bioinformatics analysts, and external users use this skill to turn Kraken2, Bracken, or compatible taxonomic abundance tables into interactive Krona-style sunburst charts for review and reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML loads external JavaScript despite offline/no-network claims.

Mitigation: Treat generated charts as network-dependent unless Plotly is embedded locally or CDN access is explicitly approved.

Risk: Python dependencies are unpinned.

Mitigation: Install in an isolated Python environment and prefer pinned, reviewed versions of pandas and plotly.

Risk: The script reads user-selected input files and writes to user-selected output paths.

Mitigation: Use intended metagenomic taxonomy report files and choose output paths carefully to avoid overwriting existing files.

## Reference(s):

- [Runtime Checklist](references/runtime_checklist.md)
- [ClawHub Skill Page](https://clawhub.ai/aipoch-ai/skills/metagenomic-krona-chart)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell commands and generated HTML chart files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated charts are HTML files; the current implementation writes Plotly output with CDN-hosted JavaScript.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
