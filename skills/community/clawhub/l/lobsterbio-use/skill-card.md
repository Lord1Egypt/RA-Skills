## Description:

Runs bioinformatics analysis with Lobster AI across single-cell RNA-seq, bulk RNA-seq, genomics, proteomics, metabolomics, machine learning, drug discovery, literature search, dataset discovery, and visualization workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cewinharhar](https://clawhub.ai/user/cewinharhar)

### License/Terms of Use:


## Use Case:

Developers, analysts, and bioinformatics practitioners use this skill to guide or orchestrate Lobster AI analyses for omics datasets, public database searches, quality control, statistical analysis, and visualization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install mutable third-party code, persist provider credentials, and send analysis work to external LLM providers and public bioinformatics services.

Mitigation: Review before installing, use an isolated environment, prefer a pinned Lobster version and only the needed domain extra, avoid global config unless necessary, and do not provide patient data, regulated identifiers, unpublished sensitive research details, or high-value API keys unless the documented network access is acceptable.

## Reference(s):

- [Agent Orchestration Patterns](references/agent-patterns.md)
- [CLI Reference](references/cli-reference.md)
- [Lobster AI PyPI Package](https://pypi.org/project/lobster-ai/)
- [Lobster CLI Documentation](https://docs.omics-os.com/raw/docs/guides/cli-commands.md)
- [Lobster Documentation Raw Page Pattern](https://docs.omics-os.com/raw/docs/{slug}.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code, markdown]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide agents to invoke Lobster CLI commands that produce JSON responses, analysis files, visualizations, and workspace configuration.]

## Skill Version(s):

1.1.406 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
