## Description: <br>
Filter compound libraries based on Lipinski's Rule of Five for drug-likeness. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, cheminformatics users, and research teams use this skill to check single SMILES strings or filter compound libraries against Lipinski's Rule of Five. It helps produce bounded, reviewable drug-likeness screening results from local compound inputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The packaged script reads local compound files and writes output files, so a mistaken path can write results somewhere the user did not intend. <br>
Mitigation: Run in a dedicated workspace, confirm input and output paths before execution, and avoid pointing output at important existing files. <br>
Risk: The RDKit dependency is declared without a pinned version in the artifact. <br>
Mitigation: Pin and audit the RDKit dependency version before use in controlled or production environments. <br>


## Reference(s): <br>
- [Lipinski Rule of Five References](references/lipinski_references.md) <br>
- [RDKit](https://www.rdkit.org/) <br>
- [RDKit Documentation](https://rdkit.readthedocs.io/) <br>
- [ClawHub Skill Page](https://clawhub.ai/aipoch-ai/lipinski-rule-filter) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, files, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples; script output includes terminal text, passed-compound files, and rule-violation reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local Python execution with RDKit for molecular property calculations; output file paths are user-selected.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
