## Description:

Analyzes consumer DNA and VCF files locally to summarize pharmacogenomics, disease risk, carrier status, ancestry, traits, and related genomics findings for AI agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wkyleg](https://clawhub.ai/user/wkyleg)

### License/Terms of Use:

MIT License

## Use Case:

Developers, AI-agent users, and genomics hobbyists use this skill to run local analysis of raw DNA exports and produce prioritized genetic findings, reports, and dashboard-ready summaries. Results are informational and should be reviewed with qualified healthcare professionals before medical decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads highly sensitive DNA files and writes derived genetic and medical reports to local storage.

Mitigation: Store input files and generated reports in an encrypted, private directory and avoid committing or sharing them.

Risk: Medication, cancer, carrier, and disease findings may be mistaken for clinical advice or diagnosis.

Mitigation: Treat outputs as informational and confirm significant findings with qualified clinicians or genetic counselors before making health or medication decisions.

Risk: Dashboard import of untrusted report files could expose users to unsafe or misleading content.

Mitigation: Load only reports generated from trusted local analyses and avoid importing reports from unknown sources.

Risk: Consumer DNA arrays and population-specific marker evidence can miss variants or produce uncertain risk estimates.

Mitigation: Communicate uncertainty, note population and chip-coverage limitations, and use clinical-grade testing for confirmation when results matter.

## Reference(s):

- [README](README.md)
- [Security Policy](SECURITY.md)
- [Genetic Results Interpretation Guide](references/INTERPRETATION_GUIDE.md)
- [DNA Testing Privacy Guide](references/PRIVACY_GUIDE.md)
- [Dashboard README](dashboard/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and descriptions of generated JSON, text, PDF, and HTML report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The underlying analysis writes local reports such as agent_summary.json, full_analysis.json, report.txt, genetic_report.pdf, and dashboard.html.]

## Skill Version(s):

4.2.0 (source: server release metadata and CHANGELOG.md, released 2026-02-07)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
