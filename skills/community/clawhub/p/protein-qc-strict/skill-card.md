## Description:

Strictest protein sequence analysis quality control workflow (3365->456 sequences), including literature validation, CD-HIT redundancy removal, complexity checks, motif verification, MSA quality assessment, and conservation/coevolution analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[billwanttobetop](https://clawhub.ai/user/billwanttobetop)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and bioinformatics practitioners use this skill to run or follow a strict protein sequence quality-control workflow before downstream alignment, phylogenetic, conservation, or coevolution analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow creates local output files and depends on conda-installed bioinformatics tools.

Mitigation: Install only in environments where CD-HIT, MAFFT, trimAl, and local file generation are acceptable.

Risk: The security summary reports correctness and path-handling weaknesses in the shell workflow.

Mitigation: Use simple trusted input and output paths until the shell quoting issue is fixed.

Risk: The security guidance says literature validation, motif verification, and coevolution claims may be advisory or incomplete.

Mitigation: Independently validate scientific claims and review quality reports before relying on results for research decisions.

## Reference(s):

- [Protein QC Strict ClawHub listing](https://clawhub.ai/billwanttobetop/skills/protein-qc-strict)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)
- [protein_qc_workflow.sh](artifact/protein_qc_workflow.sh)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and local workflow files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The workflow creates FASTA, alignment, log, and quality-report files in a user-provided output directory.]

## Skill Version(s):

4.0.0 (source: server release metadata and artifact documentation)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
