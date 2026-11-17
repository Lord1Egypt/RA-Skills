## Description:

Design multi-omics integration strategies for transcriptomics, proteomics, and metabolomics data analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, bioinformatics analysts, and research teams use this skill to plan and run pathway-level integration of transcriptomics, proteomics, and metabolomics datasets for systems biology analysis, biomarker discovery, target identification, and data quality review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Omics input files and generated outputs may contain sensitive human-subject or proprietary research data.

Mitigation: Run the skill in a controlled workspace and review generated Markdown, CSV, and JSON files before sharing them.

Risk: Dependency hygiene can affect reliability and security for local execution.

Mitigation: Install in a virtual environment or container, pin dependencies, and review packages before production use.

Risk: Pathway mappings and biological recommendations may be simplified or incomplete.

Mitigation: Treat reported pathways and recommendations as analysis support and validate important findings with domain review or follow-up experiments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aipoch-ai/skills/multi-omics-integration-strategist)
- [KEGG](https://www.genome.jp/kegg/)
- [Reactome](https://reactome.org/)
- [WikiPathways](https://www.wikipathways.org/)
- [Gene Ontology](http://geneontology.org/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, CSV tables, JSON mapping files, and terminal status text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes integration_report.md, pathway_scores.csv, mapped_ids.json, and consistency_matrix.csv to the selected output directory; visualization requires separate user-installed plotting tools.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
