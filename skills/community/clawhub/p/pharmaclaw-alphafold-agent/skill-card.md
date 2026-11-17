## Description:

Compliant AlphaFold Agent for protein structure retrieval, ESMFold prediction, binding site detection, and RDKit ligand docking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cheminem](https://clawhub.ai/user/cheminem)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and scientific workflow builders use this skill to retrieve public protein structures, run scaffolded fold prediction, detect binding pockets, and produce basic ligand docking outputs for PharmaClaw-style drug discovery pipelines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence says the skill presents mock scientific outputs as usable structure, pocket, and docking results.

Mitigation: Do not use reported structures, binding sites, or docking affinities for drug-discovery decisions unless mock paths are replaced with validated implementations and outputs carry clear provenance.

Risk: The skill performs external HTTP requests and writes predictable output files in the current working directory.

Mitigation: Run it only in a controlled working directory and review network behavior before installation or execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cheminem/skills/pharmaclaw-alphafold-agent)
- [RCSB Search API endpoint](https://search.rcsb.org/rcsbsearch/v2/query)
- [AlphaFold DB prediction API endpoint](https://alphafold.ebi.ac.uk/api/prediction/)
- [RCSB PDB file download endpoint](https://files.rcsb.org/download/{pdb_id}.pdb)

## Skill Output:

**Output Type(s):** [text, JSON, code, shell commands, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON examples; the script prints JSON reports and writes PDB or PNG files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May perform external HTTP requests and write predictable local output files such as fetched PDB files, esm_fold.pdb, and docked.png.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
