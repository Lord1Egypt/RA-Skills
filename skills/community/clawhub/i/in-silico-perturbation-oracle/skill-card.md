## Description: <br>
Provides a Python-based workflow for simulating virtual gene knockouts, differential expression, pathway enrichment, target scoring, and reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ewankeynes](https://clawhub.ai/user/ewankeynes) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and computational biology practitioners use this skill to run or adapt a virtual perturbation analysis workflow for gene knockout screening, pathway review, and target ranking. Generated biological outputs require independent validation before any research, experimental, or clinical decision. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Biomedical prediction claims may be misleading because the security evidence says the code generates simulated results while presenting them as actionable model-backed outputs. <br>
Mitigation: Treat outputs as exploratory or demo data unless real model integration, validated inputs, data provenance, and wet-lab validation are independently confirmed. <br>
Risk: Target rankings and wet-lab guidance could be misused for research, experimental, or clinical decisions. <br>
Mitigation: Require expert review and do not use generated rankings or protocols for clinical, wet-lab, or drug discovery decisions without independent validation. <br>
Risk: The workflow installs and runs Python scientific dependencies and writes files to the local filesystem. <br>
Mitigation: Install in an isolated Python environment and restrict inputs and output paths to an intended workspace. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ewankeynes/in-silico-perturbation-oracle) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Main analysis script](artifact/scripts/main.py) <br>
- [Geneformer configuration](artifact/configs/geneformer_config.yaml) <br>
- [scGPT configuration](artifact/configs/scgpt_config.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with Python and shell snippets; generated analysis files may include CSV, JSON, PNG, and text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes results to a user-selected output directory; biological outputs are simulated unless real model integration, validated inputs, and provenance are independently verified.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
