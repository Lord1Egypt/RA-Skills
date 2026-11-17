## Description:

Builds publication-quality maximum likelihood phylogenetic trees, figures, quality-control summaries, and scientific reports from FASTA sequences or enzyme-name UniProt searches.

This skill is ready for commercial/non-commercial use.

## Publisher:

[billwanttobetop](https://clawhub.ai/user/billwanttobetop)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, bioinformaticians, and AI agents use this skill to run phylogenetic analysis workflows, generate maximum likelihood trees and publication figures, and prepare structured scientific summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe R code construction around path interpolation can make untrusted paths risky.

Mitigation: Review or fix the Rscript path interpolation issue before installation, run as an unprivileged user, and use simple trusted output paths.

Risk: Feishu publishing can upload generated reports and figures to a configured bot destination.

Mitigation: Treat Feishu publishing as a separate opt-in action and confirm the lark-cli destination plus exact files before upload.

Risk: Installation guidance may modify the user's conda configuration.

Mitigation: Back up ~/.condarc before following the install guide and prefer pinned dependency files where possible.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/billwanttobetop/skills/phylo-tree)
- [UniProt](https://www.uniprot.org/)
- [Parameters Reference](references/parameters.md)
- [Installation Guide](references/installation.md)
- [AI Workflow](references/ai_workflow.md)
- [Publication Checklist](references/publication.md)
- [Troubleshooting](references/troubleshooting.md)
- [IQ-TREE Documentation](http://www.iqtree.org/doc/)
- [ggtree Documentation](https://yulab-smu.top/treedata-book/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown instructions with bash commands; generated workflow artifacts include Newick tree files, figures, JSON summaries, and Markdown reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on local bioinformatics tools, selected input mode, bootstrap settings, and configured output directory.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
