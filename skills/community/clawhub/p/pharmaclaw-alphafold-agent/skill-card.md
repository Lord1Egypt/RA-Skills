## Description: <br>
Retrieves public protein structures, predicts folds with ESMFold, detects binding pockets, and performs basic RDKit ligand docking for PharmaClaw pipeline workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Cheminem](https://clawhub.ai/user/Cheminem) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and drug discovery pipeline users use this skill to retrieve or generate protein structure artifacts and basic docking summaries from UniProt, FASTA, and SMILES inputs before passing results to downstream IP expansion or catalyst design workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Placeholder scientific calculations may be mistaken for validated protein structures, pockets, docking scores, or visualizations. <br>
Mitigation: Use only for experimentation, demos, or code review until placeholder methods are replaced with validated tools and outputs are labeled with method provenance. <br>
Risk: Unvalidated outputs could be used in research, medicinal chemistry, IP, or safety decisions. <br>
Mitigation: Do not rely on generated structures, pockets, docking scores, or visualizations for those decisions without expert review and validated scientific tooling. <br>


## Reference(s): <br>
- [RCSB Search API](https://search.rcsb.org/rcsbsearch/v2/query) <br>
- [AlphaFold DB Prediction API](https://alphafold.ebi.ac.uk/api/prediction/) <br>
- [RCSB PDB Download Endpoint](https://files.rcsb.org/download/{pdb_id}.pdb) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Files, Text] <br>
**Output Format:** [JSON report with generated PDB and PNG file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write structure and visualization files such as PDB files and docked.png in the working directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
