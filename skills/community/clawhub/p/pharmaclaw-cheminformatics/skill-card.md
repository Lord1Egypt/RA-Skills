## Description: <br>
Pharmaclaw Cheminformatics provides RDKit-based 3D conformer generation, pharmacophore mapping, molecular format conversion, RECAP fragmentation, and stereoisomer enumeration for SMILES-driven chemistry workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Cheminem](https://clawhub.ai/user/Cheminem) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, cheminformatics practitioners, and drug discovery teams use this skill to turn SMILES inputs into 3D conformer, pharmacophore, fragmentation, stereochemistry, and molecular-format analysis outputs for downstream chemistry workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Runtime dependencies for chemistry analysis can affect the local Python environment. <br>
Mitigation: Install RDKit, Pillow, and numpy from trusted sources in an isolated Python environment. <br>
Risk: The scripts can create molecular structure, coordinate, and image files at user-selected output paths. <br>
Mitigation: Use explicit project-local output paths, avoid sensitive directories, and do not run the scripts with elevated privileges. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Cheminem/pharmaclaw-cheminformatics) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Conformer generation script](artifact/scripts/conformer_gen.py) <br>
- [Pharmacophore script](artifact/scripts/pharmacophore.py) <br>
- [RECAP fragmentation script](artifact/scripts/recap_fragment.py) <br>
- [Stereoisomer enumeration script](artifact/scripts/stereoisomers.py) <br>
- [Format conversion script](artifact/scripts/format_converter.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, code, files, guidance] <br>
**Output Format:** [JSON reports with optional molecular structure, coordinate, and image files such as SDF, MOL, PDB, XYZ, SMILES, InChI, and PNG.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses SMILES or supported molecular files as inputs; optional output paths can produce local visualization and structure files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
