## Description: <br>
Generates four-tier network toxicology and molecular docking research plans from a toxicant and disease or phenotype input. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shanruoyu](https://clawhub.ai/user/shanruoyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External researchers and developers use this skill to plan computational toxicant-disease mechanism studies, including target overlap, PPI hub genes, enrichment, docking support, validation strategy, figures, and publication upgrades. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Biomedical research plans may be mistaken for validated scientific or health guidance. <br>
Mitigation: Treat outputs as research-planning aids and require expert scientific review before using them for publication, clinical, regulatory, or health-related decisions. <br>
Risk: Network target overlap, enrichment, and docking results can be overinterpreted as causal or in vivo evidence. <br>
Mitigation: Review outputs for overclaims, keep docking and enrichment language explicitly supportive, and add experimental validation before making causal claims. <br>
Risk: Target prediction, disease database bias, and weak validation datasets can produce fragile study designs. <br>
Mitigation: Use multiple target sources, document filters and overlap thresholds, apply robustness checks, and clearly label dataset validation as supportive when evidence is limited. <br>


## Reference(s): <br>
- [Workload Configurations](artifact/references/configurations.md) <br>
- [Decision Logic](artifact/references/decision-logic.md) <br>
- [Analysis Modules & Method Library](artifact/references/modules.md) <br>
- [Mandatory Output Structure](artifact/references/output-standard.md) <br>
- [Study Patterns](artifact/references/study-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown research-plan narrative with tables and structured workflow sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Always separates hypothesis generation, expression support, and docking support; includes Lite, Standard, Advanced, and Publication+ planning tiers unless the user explicitly requests a constrained single tier.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
