## Description:

Generate a personalised nutrition report from genetic data in 23andMe, AncestryDNA, or VCF format, using a local 24-gene, 28-SNP panel across 12 nutrient domains.

This skill is ready for commercial/non-commercial use.

## Publisher:

[drdaviddelorenzo](https://clawhub.ai/user/drdaviddelorenzo)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to generate local nutrigenomics reports from consumer genetic files, including nutrient risk summaries, genotype calls, visualizations, and reproducibility files. The output supports education and clinician-informed discussion, not diagnosis or medical advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive genetic data and genotype-derived reports can persist in local output directories.

Mitigation: Run the skill only on genetic files intended for local analysis, avoid shared or synced folders, and delete output directories after use.

Risk: Reports contain health-related inferences that may be misunderstood as diagnosis or medical advice.

Mitigation: Use the report for education and clinician-informed discussion, and review dietary or supplement changes with a qualified healthcare professional.

Risk: Local Python dependencies execute in the user's environment.

Mitigation: Prefer an isolated Python environment with reviewed dependencies before processing genetic files.

## Reference(s):

- [Server-resolved source import](https://github.com/drdaviddelorenzo/nutrigenomics/tree/main/skills/nutrigenomics)
- [ClawHub skill page](https://clawhub.ai/drdaviddelorenzo/skills/nutrigenomics)
- [README_OPENCLAW.md](artifact/README_OPENCLAW.md)
- [ATTRIBUTION.md](artifact/ATTRIBUTION.md)
- [SNP panel](artifact/data/snp_panel.json)
- [PubMed MEDLINE](https://pubmed.ncbi.nlm.nih.gov/)
- [GWAS Catalog](https://www.ebi.ac.uk/gwas/)
- [ClinVar](https://www.ncbi.nlm.nih.gov/clinvar/)

## Skill Output:

**Output Type(s):** [Markdown, Files, Guidance, Configuration]

**Output Format:** [Markdown report, PNG visualizations, JSON/text reproducibility files, and structured status fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are written locally under a timestamped output directory and can include per-SNP genotype calls, nutrient risk scores, figures, checksums, and provenance metadata.]

## Skill Version(s):

0.3.13 (source: evidence release, openclaw.json, CHANGELOG; SKILL.md frontmatter says 0.3.12)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
