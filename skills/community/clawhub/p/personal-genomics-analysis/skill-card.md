## Description:

Analyze consumer DNA data from WeGene, 23andMe, AncestryDNA, VCF, BAM, or CRAM files and generate evidence-based reports covering health risks, pharmacogenomics, ancestry, nutrition, exercise traits, and supplement guidance while keeping raw genetic data local.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yanzhanglee](https://clawhub.ai/user/yanzhanglee)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to analyze consumer genetic testing files locally, generate reports on genetic health risks, pharmacogenomics, nutrition, exercise, and ancestry, and prepare clinician-reviewable summaries, screening schedules, or supplement plans.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles highly sensitive genetic and health information.

Mitigation: Keep DNA files and generated reports local, store them securely, and avoid sharing full reports unless necessary.

Risk: Genetic risk, medication, and supplement guidance can be mistaken for medical diagnosis or treatment advice.

Mitigation: Present findings as risk estimates, include a clear medical disclaimer, and advise review with a qualified clinician before medication, supplement, or screening decisions.

Risk: Consumer genetic testing may have limited coverage and lower confidence than clinical-grade testing.

Mitigation: Disclose data limitations, flag missing or low-confidence variants, and recommend clinical confirmation for high-impact findings.

Risk: Optional setup commands may introduce unsafe package or environment choices.

Mitigation: Use pinned and verified packages, HTTPS reference retrieval, and an isolated virtual environment before running setup commands.

## Reference(s):

- [Supported Genetic Data Formats](artifact/references/supported_formats.md)
- [SNP Database](artifact/references/snp_database.md)
- [Supplement Guide](artifact/references/supplement_guide.md)
- [Tool Setup](artifact/references/tool_setup.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with generated Python scripts, optional shell commands, HTML reports, spreadsheet schedules, and summary documents.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports should include medical disclaimers, cite PMIDs for genetic associations, and use the user's language.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
