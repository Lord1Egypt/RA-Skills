## Description: <br>
Virtual gene knockout simulation using foundation models to predict transcriptional changes. <br>

This skill is for demonstration purposes and not for production usage. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and bioinformatics researchers use this skill to explore virtual gene knockout workflows for target screening, including simulated differential expression, pathway enrichment, target ranking, visualization reports, and wet-lab validation guide drafts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Simulated outputs may be mistaken for validated biological predictions. <br>
Mitigation: Treat scores, differential expression tables, synergy calls, and wet-lab recommendations as exploratory until genuine model inference and independent validation are in place. <br>
Risk: Biomedical inputs and generated results may be sensitive or proprietary. <br>
Mitigation: Run the skill in an isolated Python environment and avoid sensitive biomedical inputs until dependencies and data handling have been reviewed. <br>
Risk: The skill can influence wet-lab planning despite not being a validated scientific predictor. <br>
Mitigation: Require domain expert review before using outputs for experimental prioritization or protocol design. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/aipoch-ai/in-silico-perturbation-oracle-1) <br>
- [Skill documentation](artifact/SKILL.md) <br>
- [Geneformer configuration](artifact/configs/geneformer_config.yaml) <br>
- [scGPT configuration](artifact/configs/scgpt_config.yaml) <br>
- [Cell type mapping](artifact/configs/cell_type_mapping.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with shell commands and Python examples; runtime outputs include CSV, JSON, PNG, and TXT files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are written to a selected output directory and require independent scientific validation before use in experimental planning.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
