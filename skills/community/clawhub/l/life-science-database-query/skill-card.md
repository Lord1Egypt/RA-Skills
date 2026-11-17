## Description:

General life-sciences research copilot bundling 50 modular sub-skills across human genetics, variant interpretation, functional genomics, expression, pathway biology, protein structure, chemistry, clinical evidence, literature, and public study discovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sciminer](https://clawhub.ai/user/sciminer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and life-science analysts use this skill to route broad or targeted research questions to public biology, chemistry, genetics, clinical, literature, and study-discovery databases, then synthesize concise evidence-backed answers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Helper scripts allow overly broad web requests when request fields such as base_url, headers, bodies, or absolute path URLs are influenced by untrusted prompt content.

Mitigation: Install only in a constrained environment, prefer fixed public database origins, restrict network egress, and do not allow untrusted prompt content to choose request destinations or request metadata.

Risk: Raw-response save behavior can write outputs to arbitrary paths when raw_output_path is not controlled.

Mitigation: Confine raw outputs to a dedicated directory and prevent untrusted prompt content from selecting raw_output_path values.

Risk: The security verdict is suspicious because the skill is purpose-aligned but requires review before installation.

Mitigation: Review the skill before deployment and pin dependencies before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sciminer/skills/life-science-database-query)
- [Life Science Database Query skill definition](artifact/SKILL.md)
- [NCBI BLAST Common URL API notes](artifact/skills/ncbi-blast-skill/references/blast-common-url-api.txt)
- [NCBI Entrez GEO notes](artifact/skills/ncbi-entrez-skill/references/geo.md)
- [Open Targets Platform GraphQL API](https://api.platform.opentargets.org/api/v4/graphql)
- [GWAS Catalog REST API v2](https://www.ebi.ac.uk/gwas/rest/api/v2)
- [UniProt REST API](https://rest.uniprot.org)
- [ChEMBL API](https://www.ebi.ac.uk/chembl/api/data)
- [ClinicalTrials.gov API v2](https://clinicaltrials.gov/api/v2)
- [Ensembl REST API](https://rest.ensembl.org)
- [AlphaFold Protein Structure Database API](https://alphafold.ebi.ac.uk/api)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance, files]

**Output Format:** [Markdown research synthesis with optional compact JSON summaries, shell commands, and saved raw-output file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can route broad questions through the research-router or invoke individual database sub-skills for targeted lookups.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
