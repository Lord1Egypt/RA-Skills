## Description: <br>
Analyze biological data with Lobster AI, including single-cell RNA-seq, bulk RNA-seq, literature mining, dataset discovery, quality control, and visualization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cewinharhar](https://clawhub.ai/user/cewinharhar) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, developers, and bioinformatics analysts use this skill to operate Lobster AI for RNA-seq analysis, literature and dataset discovery, quality control, differential expression, cell annotation, and visualization workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installer commands rely on Lobster AI distribution endpoints, including install.lobsterbio.com. <br>
Mitigation: Confirm Lobster AI and its installer domain are trusted before installation; use the uv or pip install path when a more inspectable setup is preferred. <br>
Risk: API keys and credentials may be used during Lobster AI configuration and agent workflows. <br>
Mitigation: Use least-privilege API keys and avoid sharing credentials in prompts, workspaces, logs, or exported files. <br>
Risk: Biological datasets, downloaded files, sessions, and generated analysis outputs may persist locally. <br>
Mitigation: Keep sensitive biological data in a dedicated workspace and review local outputs before sharing or publishing them. <br>


## Reference(s): <br>
- [ClawHub Skill Release](https://clawhub.ai/cewinharhar/lobster-bio-use) <br>
- [Lobster AI Documentation](https://docs.omics-os.com) <br>
- [CLI Commands Reference](references/cli-commands.md) <br>
- [Single-Cell RNA-seq Workflow](references/single-cell-workflow.md) <br>
- [Bulk RNA-seq Workflow](references/bulk-rnaseq-workflow.md) <br>
- [Research and Dataset Discovery](references/research-workflow.md) <br>
- [Visualization Guide](references/visualization.md) <br>
- [Available Agents](references/agents.md) <br>
- [macOS and Linux Installer](https://install.lobsterbio.com) <br>
- [Windows Installer](https://install.lobsterbio.com/windows) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, analysis workflow steps] <br>
**Output Format:** [Markdown guidance with inline shell commands, slash commands, and natural-language analysis prompts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides use of Lobster AI workspaces and may lead the underlying tool to create local H5AD, HTML, PNG, CSV, JSON, Markdown, notebook, Excel, or PDF outputs.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
