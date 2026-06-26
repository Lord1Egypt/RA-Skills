## Description: <br>
Automates an AutoDock Vina molecular docking workflow from a protein PDB file, ligand SMILES string, and pocket description to top-ranked complex structures and affinity score outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[supertiefeng](https://clawhub.ai/user/supertiefeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and computational biology users can use this skill to prepare protein and ligand inputs, run AutoDock Vina docking, and collect complex structure and affinity score outputs for binding-mode prediction or ligand screening. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The docking script can run unintended local shell commands if crafted file paths or output paths are supplied. <br>
Mitigation: Review inputs before execution, use trusted paths in an isolated environment, and update subprocess calls to argument-list form with path validation before production use. <br>
Risk: The workflow relies on downloaded and locally installed docking tools. <br>
Mitigation: Install dependencies from trusted sources, verify downloaded tooling, and keep docking work directories scoped to the intended project. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/supertiefeng/molecular-docking-autodock) <br>
- [AutoDock Vina manual reference](references/autodock_vina_manual.md) <br>
- [Pocket prediction guide](references/pocket_prediction_guide.md) <br>
- [P2Rank release archive](https://github.com/rdk/p2rank/releases/download/2.4/p2rank_2.4.tar.gz) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with Python and shell command examples; generated docking outputs are PDB/PDBQT structures and score text files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local molecular docking dependencies and user-supplied protein, ligand, pocket, and output-directory parameters.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
