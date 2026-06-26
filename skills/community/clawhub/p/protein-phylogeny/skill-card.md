## Description: <br>
Comprehensive protein family phylogenetic analysis workflow with quality control, conservation analysis, coevolution network analysis, and publication-ready visualization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[billwanttobetop](https://clawhub.ai/user/billwanttobetop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and bioinformatics practitioners use this skill to analyze homologous protein sequence families, build phylogenetic trees, identify conserved and coevolved residues, and generate publication-ready figures and reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release requests unrelated high-impact capability tags, including crypto and purchase-related permissions. <br>
Mitigation: Do not grant crypto or purchase-related permissions for ordinary protein phylogeny analysis. <br>
Risk: The dependency installer can change the local host environment and install scientific packages. <br>
Mitigation: Review the installer first and run it in a container, conda environment, or other isolated environment. <br>
Risk: The workflow mentions optional Feishu/Lark export, which can upload generated reports and figures outside the local machine. <br>
Mitigation: Skip Feishu/Lark export unless the user explicitly intends to upload those outputs to that service. <br>


## Reference(s): <br>
- [Quality Control Reference](artifact/references/01-quality-control.md) <br>
- [Conservation Analysis - Shannon Entropy Method](artifact/references/02-conservation.md) <br>
- [Coevolution Analysis - Normalized Mutual Information Method](artifact/references/03-coevolution.md) <br>
- [Phylogenetic Analysis - Maximum Likelihood Method](artifact/references/04-phylogeny.md) <br>
- [Visualization - Publication-Quality Figures](artifact/references/05-visualization.md) <br>
- [Report Generation - Comprehensive Analysis Report](artifact/references/06-report.md) <br>
- [Protein Family Phylogenetic Analysis - Implementation Guide](artifact/references/IMPLEMENTATION.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash, Python, and R commands; generated workflow artifacts include FASTA, CSV, JSON, PNG, PDF, SVG, Newick/tree files, and Markdown reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local analysis artifacts under the chosen output directory; optional Feishu/Lark export is user-initiated.] <br>

## Skill Version(s): <br>
1.5.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
