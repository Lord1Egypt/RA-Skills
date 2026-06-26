## Description: <br>
Chemistry agent skill for public compound lookups, RDKit cheminformatics, molecule visualization, reaction simulation, retrosynthesis, synthesis route planning, and advanced descriptor and scaffold analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Cheminem](https://clawhub.ai/user/Cheminem) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and chemistry-focused agents use this skill to query public chemistry and literature databases, calculate molecular properties, generate molecule visualizations, and produce structured outputs for downstream drug-discovery workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: External lookup features can send compound names, structures, or research terms to public chemistry and literature services. <br>
Mitigation: Avoid external lookups for proprietary or unpublished research inputs; prefer local RDKit-only actions when sensitive compounds are involved. <br>
Risk: The skill can create local output files and may optionally download and run the OPSIN Java helper. <br>
Mitigation: Run it in a controlled local environment, keep file outputs in expected project directories, and rely on the provided checksum verification before using OPSIN. <br>
Risk: Computed descriptors, retrosynthesis fragments, reaction products, and ADMET rule checks are decision-support outputs, not validated experimental conclusions. <br>
Mitigation: Review results with qualified chemistry expertise and corroborate important findings against trusted literature or experimental data. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Cheminem/pharmaclaw-chemistry-query) <br>
- [PubChem API Endpoints](references/api_endpoints.md) <br>
- [PubChem PUG REST Documentation](https://pubchemdocs.ncbi.nlm.nih.gov/pug-rest) <br>
- [ChEMBL API](https://www.ebi.ac.uk/chembl/api/data) <br>
- [NCBI E-utilities](https://eutils.ncbi.nlm.nih.gov/entrez/eutils) <br>
- [OPSIN CLI Release](https://github.com/dan2097/opsin/releases/download/2.8.0/opsin-cli-2.8.0-jar-with-dependencies.jar) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [JSON responses, Markdown guidance, shell command examples, and generated PNG, SVG, XYZ, CSV, or text files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include public API query results, RDKit descriptors, molecule drawings, retrosynthesis fragments, reaction products, and agent-chain JSON.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release evidence; artifact changelog top entry is v2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
