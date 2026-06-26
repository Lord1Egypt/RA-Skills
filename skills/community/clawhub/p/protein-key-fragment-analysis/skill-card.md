## Description: <br>
Analyzes multi-species protein FASTA inputs to derive consensus sequences, identify conserved key fragments, summarize amino acid composition, and predict likely fragment functions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wuhen9nine](https://clawhub.ai/user/wuhen9nine) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and bioinformatics analysts use this skill to run local protein key-fragment analysis over FASTA sequence sets and produce conserved-region, composition, and predicted-function summaries. It is intended for protein family exploration and comparative analysis, with biological claims requiring domain review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Predicted functional regions and disulfide-bond interpretations may be biologically incorrect or incomplete. <br>
Mitigation: Treat generated claims as computational predictions and validate them with domain expertise, curated databases, or experimental evidence before using them for scientific or operational decisions. <br>
Risk: MSA-based analysis can fail or produce incomplete results when the clustalo system dependency is unavailable. <br>
Mitigation: Install and verify Clustal Omega before running full analysis workflows, and document the installed version in reproducible analyses. <br>
Risk: Some documentation references optional combined aa-pair workflows that are not included in this package. <br>
Mitigation: Scope use to the packaged key-fragment analysis workflow unless the missing aa-pair workflow is separately installed and reviewed. <br>
Risk: Threshold choices can materially change the biological interpretation of conserved regions. <br>
Mitigation: Record consensus and key-fragment thresholds with each run and review sensitivity when comparing species or protein families. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wuhen9nine/protein-key-fragment-analysis) <br>
- [Method reference](references/method.md) <br>
- [Functional domains reference](references/functional_domains.md) <br>
- [Fibrinogen domains reference](references/fibrinogen_domains.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, JSON key-fragment files, FASTA-derived text outputs, and shell/configuration guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create per-species analysis reports and key-fragment JSON files; local FASTA inputs and the clustalo system dependency are required for full MSA-based analysis.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence and artifact skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
