## Description: <br>
Design multi-omics integration strategies for transcriptomics, proteomics, and metabolomics data analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Bioinformatics researchers, computational biologists, and developers use this skill to plan and run pathway-level integration of transcriptomics, proteomics, and metabolomics datasets for mechanism research, biomarker discovery, drug target analysis, and data quality checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Input omics datasets and generated analysis outputs may contain sensitive local research data. <br>
Mitigation: Run the skill in a controlled local workspace, restrict access to the output directory, and handle generated files according to the user's data governance requirements. <br>
Risk: Dependencies are not pinned in the artifact requirements file. <br>
Mitigation: Install in a virtual environment and pin dependency versions before production or regulated use. <br>
Risk: The script creates files in the selected output directory. <br>
Mitigation: Choose the output path intentionally and review generated files before sharing or retaining them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aipoch-ai/multi-omics-integration-strategist) <br>
- [KEGG](https://www.genome.jp/kegg/) <br>
- [Reactome](https://reactome.org/) <br>
- [WikiPathways](https://www.wikipathways.org/) <br>
- [Gene Ontology](http://geneontology.org/) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python command examples plus generated local CSV, JSON, and Markdown analysis files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads local CSV omics datasets and writes result files to a user-selected output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
