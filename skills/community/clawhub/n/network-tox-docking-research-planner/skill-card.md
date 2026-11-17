## Description:

Generates four-tier network toxicology and molecular docking research plans from a toxicant-disease input, including target and pathway analysis, docking strategy, validation planning, figures, and a publication upgrade path.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shanruoyu](https://clawhub.ai/user/shanruoyu)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers and technical writers use this skill to draft computational toxicant-disease mechanism study plans. It helps structure network toxicology, molecular docking, validation, figure, and publication planning without executing the analyses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Outputs are study designs, not clinical advice or proof of biological causality.

Mitigation: Keep conclusions framed as computational hypotheses and require domain review before using the plan for claims, submissions, or experimental decisions.

Risk: The skill may activate on casual chemical-and-disease research requests.

Mitigation: Confirm the request involves a toxicant-disease or toxicant-phenotype research-planning task before applying the workflow.

Risk: Target prediction, disease database overlap, pathway enrichment, and docking can be overinterpreted.

Mitigation: Use multiple target sources, separate network, expression, enrichment, and docking evidence layers, and state what each layer does and does not prove.

Risk: No executable code or hidden system changes were found, but generated plans can still include external tools and databases.

Mitigation: Review proposed tools, datasets, thresholds, and validation steps before execution in a research environment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/shanruoyu/skills/network-tox-docking-research-planner)
- [Decision Logic](artifact/references/decision-logic.md)
- [Study Patterns](artifact/references/study-patterns.md)
- [Workload Configurations](artifact/references/configurations.md)
- [Analysis Modules & Method Library](artifact/references/modules.md)
- [Mandatory Output Structure](artifact/references/output-standard.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown research plan with structured sections and tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs four workload configurations, a recommended primary plan, workflow steps, validation strategy, figure plan, minimal executable version, and publication upgrade path.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
