## Description:

Performs GO (Gene Ontology) and KEGG pathway enrichment analysis on gene lists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT

## Use Case:

Developers, bioinformaticians, and research teams use this skill to run GO and KEGG enrichment analysis on gene lists, including differentially expressed genes, and produce statistical results, visualizations, and biological summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Online enrichment modes and KEGG queries can expose submitted gene lists to external services.

Mitigation: Do not use --use-enrichr or KEGG/online modes with confidential, regulated, or pre-publication gene lists unless external submission is authorized.

Risk: The security review reports an unsafe plotting evaluation path.

Mitigation: Review or fix the plotting eval() path before installation or execution.

Risk: Local execution reads input files, writes result files, and depends on scientific Python/R packages.

Mitigation: Run the skill in an isolated virtual environment with pinned dependencies and direct output to a dedicated results folder.

## Reference(s):

- [GO/KEGG Enrichment skill page](https://clawhub.ai/aipoch-ai/skills/go-kegg-enrichment)
- [GO/KEGG Enrichment Analysis References](artifact/references/GO_KEGG_Reference.md)
- [Example gene list](artifact/references/example_gene_list.txt)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and generated analysis files such as CSV, TSV, Excel, PNG, and text reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill writes enrichment result tables, plots, and a human-readable report to the selected output directory.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
