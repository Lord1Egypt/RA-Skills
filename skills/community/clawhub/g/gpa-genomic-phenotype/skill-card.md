## Description: <br>
GPA Genomic Phenotype Association helps agents run genomic variant and phenotype association analysis with tissue-aware tiering for germline risk, somatic tumor variants, pharmacogenomics, and multi-hit findings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lzr098](https://clawhub.ai/user/lzr098) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and genomics analysts use this skill to run variant files or variant JSON through GPA after confirming analysis purpose, sample identity, and phenotype or tissue context. It produces tiered decision-support reports and structured results that require qualified clinical review before use in patient or regulated settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive genetic and phenotype data may be sent to external services or retained in local cache, log, or output files. <br>
Mitigation: Use offline mode for sensitive samples when possible, avoid identifiers in phenotype text, obtain appropriate consent for external processing, and protect or clear cache, log, and output directories after use. <br>
Risk: Generated genomic reports may be mistaken for standalone diagnosis or treatment advice. <br>
Mitigation: Treat outputs as decision support only and require review by qualified clinical personnel before patient-facing or regulated use. <br>
Risk: Proxy environment settings can route sensitive network traffic through unintended infrastructure. <br>
Mitigation: Review HTTP_PROXY and HTTPS_PROXY settings before running analyses that may contact external services. <br>


## Reference(s): <br>
- [GPA Skill Page](https://clawhub.ai/lzr098/gpa-genomic-phenotype) <br>
- [GPA README](artifact/README.md) <br>
- [Phase Analysis Algorithm](artifact/docs/PHASE_ANALYSIS_ALGORITHM.md) <br>
- [Runtime Configuration](artifact/references/dgra.yaml) <br>
- [Gene Phenotype Map](artifact/references/gene_phenotype_map.json) <br>
- [Tissue Context Reference](artifact/references/tissue_context.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports and structured JSON results, with shell command examples for running the GPA wrapper.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include tier summaries, variant evidence chains, QC flags, multi-hit details, and analysis metadata.] <br>

## Skill Version(s): <br>
0.8.0 (source: server release metadata and artifact config.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
