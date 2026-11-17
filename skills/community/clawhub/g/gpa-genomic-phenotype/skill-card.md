## Description:

GPA (Genomic Phenotype Association) analyzes genomic variants against phenotype and tissue context using external biomedical annotations, offline fallback data, tiered risk classification, multi-hit and phase analysis, ClinVar confidence handling, gnomAD frequency lookup, and optional SpliceAI splice prediction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lzr098](https://clawhub.ai/user/lzr098)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, clinical informatics teams, and genomics analysts use this skill to run structured gene-phenotype association and variant tiering workflows for germline risk, somatic tumor analysis, pharmacogenomics, multi-hit detection, and tissue-specific review. The reports are decision-support artifacts and require qualified clinical review before use in care decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive genomic, phenotype, or patient-identifiable data may be sent to external biomedical services during online analysis.

Mitigation: Use offline mode by default for patient or identifiable data and enable external API calls only after privacy review and user authorization.

Risk: Genomic caches can retain sensitive analysis data after a run.

Mitigation: Run the skill in an isolated environment and clear, encrypt, or otherwise protect cache directories after sensitive analyses.

Risk: Variant tiering and phenotype association results can be mistaken for definitive clinical advice.

Mitigation: Treat outputs as decision support and require review by qualified clinical or genomics professionals before care decisions.

Risk: Scenario ambiguity can change how the same variant is classified.

Mitigation: Confirm analysis purpose, sample identity, and disease or tissue context before executing analysis or producing a report.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lzr098/skills/gpa-genomic-phenotype)
- [README](artifact/README.md)
- [Phase Analysis Algorithm](artifact/docs/PHASE_ANALYSIS_ALGORITHM.md)
- [Runtime Configuration](artifact/references/dgra.yaml)
- [Ensembl REST API](https://rest.ensembl.org)
- [UniProt REST API](https://rest.uniprot.org)
- [GTEx Portal API](https://gtexportal.org/api/v2)
- [gnomAD GraphQL API](https://gnomad.broadinstitute.org/api)
- [NCBI E-utilities](https://eutils.ncbi.nlm.nih.gov/entrez/eutils)
- [HGNC REST API](https://rest.genenames.org)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, JSON results, and command-line guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include tiered variant findings, evidence chains, phenotype association details, QC flags, and optional saved Markdown or JSON files.]

## Skill Version(s):

0.8.0 (source: server release metadata, artifact/config.json, changelog released 2026-05-23)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
