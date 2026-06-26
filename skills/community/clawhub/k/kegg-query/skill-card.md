## Description: <br>
Query KEGG database for drug information, pathway analysis, and disease-drug-target discovery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hollyya](https://clawhub.ai/user/hollyya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and biomedical analysts use this skill to retrieve KEGG drug, pathway, compound, gene, and disease information for lookup, pathway analysis, and disease-drug-target discovery workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Biomedical queries may be sent to public KEGG services, and optional integrations may send related identifiers to UniProt or OpenBioMed tooling. <br>
Mitigation: Avoid private patient data and confidential research queries; use public or approved biomedical identifiers only. <br>
Risk: KEGG results can be incomplete, stale, or unsuitable as medical advice. <br>
Mitigation: Treat returned data as reference information and have qualified experts verify clinical or research conclusions. <br>
Risk: Large or repeated lookups can exceed KEGG service expectations. <br>
Mitigation: Respect KEGG rate limits and add delays or batching controls for larger workflows. <br>


## Reference(s): <br>
- [KEGG Databases Reference](references/kegg_databases.md) <br>
- [KEGG API Operations Reference](references/kegg_api_operations.md) <br>
- [KEGG API Documentation](https://www.kegg.jp/kegg/rest/keggapi.html) <br>
- [ClawHub Skill Page](https://clawhub.ai/hollyya/kegg-query) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with Python examples, KEGG REST request patterns, and structured JSON result shapes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May involve public KEGG REST API calls and optional UniProt/OpenBioMed integration when used by an agent.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
