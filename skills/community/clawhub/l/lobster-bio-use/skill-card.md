## Description:

Guides agents in using Lobster AI for biological data analysis, including single-cell and bulk RNA-seq, literature and dataset discovery, quality control, differential expression, and visualization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cewinharhar](https://clawhub.ai/user/cewinharhar)

### License/Terms of Use:


## Use Case:

External researchers, bioinformatics practitioners, and developers use this skill to operate Lobster AI for transcriptomics analysis, literature and dataset discovery, quality control, differential expression, and visualization workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup guidance includes remote installer commands executed directly in the shell.

Mitigation: Review the installer path before use and prefer verified, version-pinned package-manager installation in an isolated, non-admin environment.

Risk: Lobster configuration and analysis workflows may store API keys, downloaded datasets, and generated analysis outputs in local workspaces.

Mitigation: Use a dedicated workspace, protect credentials, and review generated files before sharing or committing them.

## Reference(s):

- [CLI Commands Reference](references/cli-commands.md)
- [Single-Cell RNA-seq Workflow](references/single-cell-workflow.md)
- [Bulk RNA-seq Workflow](references/bulk-rnaseq-workflow.md)
- [Research & Dataset Discovery](references/research-workflow.md)
- [Visualization Guide](references/visualization.md)
- [Available Agents](references/agents.md)
- [Lobster AI Documentation](https://docs.omics-os.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline command examples and workflow steps.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide creation of local analysis outputs such as H5AD, HTML, PNG, CSV, and JSON files through Lobster AI.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
