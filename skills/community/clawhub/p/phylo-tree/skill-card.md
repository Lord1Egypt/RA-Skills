## Description: <br>
Phylo Tree helps agents run maximum likelihood phylogenetic analysis from FASTA sequences or an optional UniProt query and produce trees, figures, summaries, and report material. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[billwanttobetop](https://clawhub.ai/user/billwanttobetop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and AI agents use this skill to prepare publication-oriented phylogenetic tree analyses, especially from local FASTA inputs, and to generate structured summaries and report-ready outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Crafted output paths may lead to injected R code execution in some scripts. <br>
Mitigation: Use simple, trusted output paths without quotes or unusual characters and review scripts before running them on untrusted inputs. <br>
Risk: Installation guidance can make persistent changes to conda configuration. <br>
Mitigation: Use an isolated conda environment and back up ~/.condarc before applying solver or channel changes. <br>
Risk: The Feishu/Lark report helper can publish reports and figures through a configured bot account. <br>
Mitigation: Run generate_feishu_report.py only when cloud publication is intended and the target account and document permissions are understood. <br>
Risk: Query mode contacts the UniProt API and depends on external service behavior. <br>
Mitigation: Prefer --fasta mode for offline, reproducible analysis unless network access to UniProt is explicitly acceptable. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/billwanttobetop/phylo-tree) <br>
- [AI Workflow](references/ai_workflow.md) <br>
- [Parameters Reference](references/parameters.md) <br>
- [Installation Guide](references/installation.md) <br>
- [Publication Checklist](references/publication.md) <br>
- [UniProt](https://www.uniprot.org/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command examples plus generated analysis files such as JSON summaries, Newick tree files, PNG figures, and report drafts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The normal workflow runs locally with FASTA input; UniProt API access is optional when query mode is used.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
