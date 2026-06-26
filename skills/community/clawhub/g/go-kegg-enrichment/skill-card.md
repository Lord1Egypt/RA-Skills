## Description: <br>
Performs GO and KEGG pathway enrichment analysis on gene lists and generates enriched terms, statistics, visualizations, and summary reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AIPOCH-AI](https://clawhub.ai/user/AIPOCH-AI) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, bioinformatics analysts, and researchers use this skill to run GO and KEGG enrichment workflows for gene lists, including differentially expressed genes, and review tabular results, plots, and an interpretation report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unsafe dynamic evaluation is used while parsing enrichment ratio values. <br>
Mitigation: Review or patch the ratio parsing before installation, and run the skill only in an isolated project environment. <br>
Risk: Online Enrichr workflows can transfer gene-list data outside the local workspace. <br>
Mitigation: Avoid Enrichr or other online workflows for unpublished, proprietary, or clinical gene lists unless external data transfer is explicitly approved. <br>
Risk: The script reads user-selected input paths and writes output directories. <br>
Mitigation: Keep input and output paths inside the intended workspace and review generated result files before sharing. <br>


## Reference(s): <br>
- [GO/KEGG Enrichment ClawHub page](https://clawhub.ai/AIPOCH-AI/go-kegg-enrichment) <br>
- [GO/KEGG Reference](references/GO_KEGG_Reference.md) <br>
- [Example Gene List](references/example_gene_list.txt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Command-line guidance plus generated CSV, TSV, Excel, PNG, and text report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes GO and KEGG result tables, visualizations, and REPORT.txt under the selected output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
