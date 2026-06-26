## Description: <br>
Professional protein sequence quality control and visualization workflow with a complete QC pipeline, conservation and coevolution analysis, and publication-ready figure generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[billwanttobetop](https://clawhub.ai/user/billwanttobetop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and researchers use this skill to run protein-family sequence quality control, generate alignment and conservation analyses, and produce publication-ready figures for downstream phylogenetic or enzyme-engineering work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan reports that the workflow is tied to a hard-coded local research environment and does not match its advertised generic command-line usage. <br>
Mitigation: Review before installing, run only in a disposable or well-understood workspace, and parameterize scripts with explicit input and output paths before using them on local data. <br>
Risk: The security guidance flags shell command strings and hard-coded /root/autodl-tmp paths as concrete implementation risks. <br>
Mitigation: Remove hard-coded paths and replace shell=True command execution with argument-list subprocess calls before production use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/billwanttobetop/protein-sequence-qc-pro) <br>
- [Artifact README](artifact/README.md) <br>
- [Skill documentation](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Analysis, Files, Guidance] <br>
**Output Format:** [Markdown guidance with bash examples and generated analysis files, figures, JSON, CSV, FASTA, PNG, and PDF outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3, CD-HIT, MAFFT, trimAl, Biopython, NumPy, and Matplotlib.] <br>

## Skill Version(s): <br>
5.0.0 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
