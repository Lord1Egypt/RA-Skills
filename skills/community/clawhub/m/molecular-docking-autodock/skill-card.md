## Description:

Automates AutoDock Vina protein-small molecule docking from a PDB protein file, ligand SMILES, and pocket description, producing top docked complex structures and docking score results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[supertiefeng](https://clawhub.ai/user/supertiefeng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and computational chemistry practitioners use this skill to prepare protein and ligand inputs, configure a binding pocket, run AutoDock Vina docking, and review predicted binding poses and affinity scores.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted protein, output, or generated file paths may cause unintended shell command execution in the docking script.

Mitigation: Run the skill only in an isolated, unprivileged environment and avoid untrusted paths until shell commands are converted to argument-list subprocess calls with constrained paths.

Risk: The P2Rank dependency is downloaded externally during setup.

Mitigation: Pin dependencies and verify the P2Rank archive before use.

Risk: Text-described pocket prediction can select an offset or unintended binding pocket.

Mitigation: Prefer explicit pocket coordinates or residue ranges for important runs and review the predicted binding mode before acting on results.

## Reference(s):

- [AutoDock VINA usage reference](references/autodock_vina_manual.md)
- [Pocket description and prediction guide](references/pocket_prediction_guide.md)
- [P2Rank 2.4 release archive](https://github.com/rdk/p2rank/releases/download/2.4/p2rank_2.4.tar.gz)

## Skill Output:

**Output Type(s):** [Files, Text, Shell commands, Configuration instructions]

**Output Format:** [Markdown guidance plus generated PDB/PDBQT structures, Vina config, docking log, and tabular score text files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include the top docked complex structure, ligand pose files, docking_scores.txt, and optional visualization assets when dependencies are available.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
