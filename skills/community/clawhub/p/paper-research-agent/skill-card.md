## Description:

Paper Research Agent orchestrates academic literature search, arXiv PDF download, parallel full-paper analysis, and integrated survey generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[changer-changer](https://clawhub.ai/user/changer-changer)

### License/Terms of Use:

MIT-0

## Use Case:

External researchers, developers, and agents use this skill to find academic papers, download arXiv PDFs, create structured per-paper analyses, compare methods, and generate integrated literature surveys.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can modify the Python environment by installing dependencies automatically.

Mitigation: Run it in a sandboxed workspace with pinned dependencies preinstalled and review dependency changes before execution.

Risk: The workflow contacts external servers and can download and store many PDFs.

Mitigation: Use restricted network access, file-size and output limits, and explicit approval before downloads.

Risk: The workflow creates sub-agent tasks for parallel full-paper analysis.

Mitigation: Require explicit approval and limits for sub-agent spawning, then manually review critical citations and extracted data.

## Reference(s):

- [Paper Analysis Report Standards](references/analysis_standards.md)
- [ClawHub Skill Page](https://clawhub.ai/changer-changer/skills/paper-research-agent)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, JSON summaries, shell command snippets, and downloaded PDF files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates a research output directory with paper PDFs, per-paper analysis reports, agent task JSON, and an integrated survey.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
