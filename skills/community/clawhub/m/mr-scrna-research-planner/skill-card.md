## Description:

Generates structured Mendelian Randomization plus single-cell RNA-seq research designs from a user-provided biomedical research direction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External biomedical researchers and bioinformatics practitioners use this skill to design computational MR plus scRNA-seq studies with workload options, a recommended primary plan, validation strategy, figure plan, and publication upgrade path.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may mistake biomedical research plans for clinical, medical, regulatory, or prescriptive advice.

Mitigation: Use outputs only for computational research planning and independently verify all biological claims, datasets, tool choices, and causal interpretations.

Risk: MR and scRNA-seq findings can be overinterpreted when associative single-cell evidence is presented as causal evidence.

Mitigation: Keep correlation-level and causal-level evidence separate, and require experimental or clinical validation before applying causal interpretations.

Risk: Study designs may depend on unsuitable public datasets, weak instruments, or missing validation cohorts.

Mitigation: Check dataset fit, instrument strength, ancestry compatibility, and validation availability before executing a proposed plan.

## Reference(s):

- [Analysis Module Library](references/analysis-modules.md)
- [Figure and Deliverable Plan](references/figure-deliverable-plan.md)
- [Method Library](references/method-library.md)
- [Study Patterns](references/study-patterns.md)
- [Validation and Evidence Hierarchy](references/validation-evidence-hierarchy.md)
- [Workflow Step Template](references/workflow-step-template.md)
- [Workload Configurations](references/workload-configurations.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Structured Markdown research plan with tables and sectioned workflow]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes four workload configurations, one recommended primary plan, validation strategy, figure plan, minimal executable version, and publication upgrade path.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
