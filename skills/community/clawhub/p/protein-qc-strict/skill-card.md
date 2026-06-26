## Description: <br>
Strict protein sequence quality-control workflow for protein family analysis, including literature validation, CD-HIT redundancy removal, complexity checks, motif verification, MSA quality assessment, and conservation and co-evolution analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[billwanttobetop](https://clawhub.ai/user/billwanttobetop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and bioinformatics analysts use this skill to prepare protein family sequence sets for publication-quality analysis through staged filtering, redundancy removal, motif checks, alignment, trimming, and QC reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow runs shell commands and third-party bioinformatics tools against user-provided sequence files. <br>
Mitigation: Run it in a controlled conda or container environment, review the generated commands before execution, and use trusted input FASTA files. <br>
Risk: Scientific conclusions can be misleading if sequence provenance, motif assumptions, or gap-heavy alignment positions are not independently checked. <br>
Mitigation: Verify literature support, inspect each QC report, and review high-gap sites and threshold choices before using results in publication or downstream analysis. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/billwanttobetop/protein-qc-strict) <br>
- [Artifact README](artifact/README.md) <br>
- [Skill documentation](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash and Python examples plus workflow-generated FASTA, alignment, log, and quality-report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The workflow expects an input FASTA file and an output directory, and depends on CD-HIT, MAFFT, trimAl, Python, BioPython, and NumPy.] <br>

## Skill Version(s): <br>
4.0.0 (source: server release evidence and skill documentation) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
