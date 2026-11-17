## Description:

Chemistry agent skill for PubChem API queries, RDKit cheminformatics, molecular visualization, retrosynthesis, reaction simulation, ADMET-style screening, and public biomedical chemistry lookups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cheminem](https://clawhub.ai/user/cheminem)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and chemistry-focused agents use this skill to retrieve compound data, compute molecular descriptors, visualize structures, plan retrosynthesis routes, run reaction templates, and query public chemistry or biomedical APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can contact public chemistry and biomedical APIs.

Mitigation: Run it with network access appropriate for the workspace and avoid sending sensitive or regulated compound data to public services.

Risk: The skill can read input files and write generated outputs.

Mitigation: Run it in a restricted workspace and constrain input and output paths before using file-based options.

Risk: IUPAC name conversion downloads and executes an OPSIN Java JAR on first use.

Mitigation: Review the dependency, rely on the pinned checksum verification, and disable or pre-stage OPSIN where executable downloads are not allowed.

Risk: The Gradio interface could expose chemistry tooling to unintended users if hosted broadly.

Mitigation: Keep the UI local or place it behind trusted access controls; do not expose it to untrusted users.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cheminem/skills/pharmaclaw-chemistry-query)
- [PubChem API Endpoints](references/api_endpoints.md)
- [PubChem PUG REST Documentation](https://pubchemdocs.ncbi.nlm.nih.gov/pug-rest)
- [PubChem PUG REST API](https://pubchem.ncbi.nlm.nih.gov/rest/pug)
- [PubChem PUG View API](https://pubchem.ncbi.nlm.nih.gov/rest/pug_view)
- [ChEMBL API](https://www.ebi.ac.uk/chembl/api/data)
- [NCBI E-utilities](https://eutils.ncbi.nlm.nih.gov/entrez/eutils)
- [OPSIN CLI Release](https://github.com/dan2097/opsin/releases/download/2.8.0/opsin-cli-2.8.0-jar-with-dependencies.jar)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [JSON reports, Markdown guidance with shell commands, and generated PNG/SVG/CSV/XYZ files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May contact public chemistry and biomedical APIs, write local output files, and download a checksum-pinned OPSIN Java JAR on first IUPAC name conversion.]

## Skill Version(s):

2.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
