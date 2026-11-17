## Description:

Comprehensive workflow for protein family phylogenetic analysis, including sequence quality control, conservation and coevolution analysis, tree reconstruction, visualization, and report generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[billwanttobetop](https://clawhub.ai/user/billwanttobetop)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, bioinformatics practitioners, and research teams use this skill to run a protein family evolutionary analysis workflow from FASTA inputs through quality-controlled alignments, conservation and coevolution results, phylogenetic trees, figures, and reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency installation may invoke privileged package managers or download bioinformatics binaries without built-in verification.

Mitigation: Install in an isolated container, virtual machine, or dedicated conda/venv; avoid sudo where possible and verify downloaded binaries before use.

Risk: Publishing guidance can upload generated reports and figures to Feishu/Lark.

Mitigation: Use upload steps only when data sharing is intended and approved for the research outputs being processed.

Risk: Poor-quality or unsuitable sequence inputs can lead to misleading conservation, coevolution, or phylogenetic conclusions.

Mitigation: Review quality-control outputs, alignment quality, bootstrap support, and documented method assumptions before using results for downstream decisions.

## Reference(s):

- [Quality Control Reference](references/01-quality-control.md)
- [Conservation Analysis - Shannon Entropy Method](references/02-conservation.md)
- [Coevolution Analysis - Mutual Information Method](references/03-coevolution.md)
- [Phylogenetic Analysis - Maximum Likelihood Method](references/04-phylogeny.md)
- [Visualization - Publication-Quality Figures](references/05-visualization.md)
- [Report Generation - Comprehensive Analysis Report](references/06-report.md)
- [Protein Family Phylogenetic Analysis - Implementation Guide](references/IMPLEMENTATION.md)
- [Complete Installation and Usage Test](TESTING.md)
- [ClawHub skill page](https://clawhub.ai/billwanttobetop/skills/protein-phylogeny)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash, Python, and R command examples; workflow outputs include CSV, JSON, figures, tree files, and Markdown reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local analysis artifacts under the selected output directory.]

## Skill Version(s):

1.5.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
