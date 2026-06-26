## Description: <br>
Chemistry agent skill for PubChem API queries and RDKit cheminformatics, including compound lookup, molecular properties, structure images, fingerprints, retrosynthesis, reaction simulation, and synthesis planning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cheminempharmaclaw](https://clawhub.ai/user/cheminempharmaclaw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and cheminformatics teams use this skill to query public chemistry data, analyze SMILES or compound names with RDKit, generate molecule visualizations, and produce structured results for downstream chemistry or pharmacology workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Compound names, SMILES strings, and literature queries may be sent to public chemistry APIs. <br>
Mitigation: Use offline-only RDKit actions for confidential compounds, or avoid name and literature lookups when public API disclosure is not acceptable. <br>
Risk: The skill can write local chemistry output files such as molecule images, descriptors, coordinate files, CSV, JSON, or text. <br>
Mitigation: Run it in an approved workspace, review requested output paths, and retain only generated files needed for the workflow. <br>
Risk: IUPAC name conversion can download and run the OPSIN Java JAR on first use. <br>
Mitigation: Allow this feature only where Java execution and the checksum-verified OPSIN download are acceptable, or disable OPSIN-dependent actions. <br>
Risk: Optional lab integration can expand the operational surface when used with pharmaclaw-lab-ui. <br>
Mitigation: Review or disable the optional lab_hook integration before use in environments that do not require it. <br>


## Reference(s): <br>
- [PubChem API Endpoints](references/api_endpoints.md) <br>
- [PubChem PUG REST documentation](https://pubchemdocs.ncbi.nlm.nih.gov/pug-rest) <br>
- [PubChem PUG REST API](https://pubchem.ncbi.nlm.nih.gov/rest/pug) <br>
- [ChEMBL API](https://www.ebi.ac.uk/chembl/api/data) <br>
- [NCBI E-utilities](https://eutils.ncbi.nlm.nih.gov/entrez/eutils) <br>
- [OPSIN CLI release](https://github.com/dan2097/opsin/releases/download/2.8.0/opsin-cli-2.8.0-jar-with-dependencies.jar) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, files] <br>
**Output Format:** [Structured JSON with optional PNG, SVG, XYZ, CSV, or text output files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call public chemistry APIs and may create local visualization or data files when requested.] <br>

## Skill Version(s): <br>
2.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
