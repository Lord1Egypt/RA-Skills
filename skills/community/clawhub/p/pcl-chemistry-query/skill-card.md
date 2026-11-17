## Description:

PharmaClaw Chemistry Query helps agents query public chemistry APIs and run RDKit-based cheminformatics analysis for compounds, structures, SMILES, reactions, retrosynthesis, and synthesis planning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cheminempharmaclaw](https://clawhub.ai/user/cheminempharmaclaw)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and chemistry-focused agents use this skill to retrieve compound data from PubChem, ChEMBL, and PubMed and run RDKit analysis, visualization, ADMET checks, similarity search, retrosynthesis, and synthesis planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends compound names, SMILES strings, and search terms to public chemistry APIs.

Mitigation: Use only non-sensitive chemistry queries and avoid submitting proprietary or confidential compound information.

Risk: IUPAC name conversion downloads the OPSIN JAR at runtime before executing it.

Mitigation: Run in an isolated workspace and rely on the pinned checksum verification before permitting OPSIN execution.

Risk: scripts/chain_entry.py attempts to import lab_hook from a neighboring pharmaclaw-lab-ui folder.

Mitigation: Avoid scripts/chain_entry.py until that import is removed or the neighboring code is explicitly reviewed and trusted.

Risk: File path options such as input_file and output can read or write files available to the agent.

Mitigation: Do not provide sensitive local file paths, and run the skill with limited filesystem access.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cheminempharmaclaw/skills/pcl-chemistry-query)
- [PubChem API Endpoints](references/api_endpoints.md)
- [PubChem PUG REST documentation](https://pubchemdocs.ncbi.nlm.nih.gov/pug-rest)
- [PubChem PUG REST API](https://pubchem.ncbi.nlm.nih.gov/rest/pug)
- [PubChem PUG View API](https://pubchem.ncbi.nlm.nih.gov/rest/pug_view)
- [ChEMBL API](https://www.ebi.ac.uk/chembl/api/data)
- [NCBI E-utilities](https://eutils.ncbi.nlm.nih.gov/entrez/eutils)
- [OPSIN CLI release](https://github.com/dan2097/opsin/releases/download/2.8.0/opsin-cli-2.8.0-jar-with-dependencies.jar)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Files, Guidance]

**Output Format:** [Markdown guidance with command examples; invoked scripts return structured JSON and optional PNG, SVG, XYZ, CSV, or text files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call public chemistry APIs and may write local visualization or analysis files when output paths are supplied.]

## Skill Version(s):

2.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
