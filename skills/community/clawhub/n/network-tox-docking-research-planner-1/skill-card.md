## Description:

Generates complete network toxicology and molecular docking research designs from a user-provided toxicant and disease or phenotype.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, scientific writers, and external users use this skill to plan computational toxicant-disease mechanism studies with target prediction, PPI hub-gene analysis, enrichment, docking support, validation planning, figures, and publication upgrade paths.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can produce research-planning guidance that users might mistake for clinical, regulatory, experimental, or causal proof.

Mitigation: Treat outputs as computational study plans only; require expert review and experimental validation before making causal, clinical, regulatory, or safety claims.

Risk: Broad toxicant-disease prompts may steer the agent into a network toxicology and docking plan even when another study type or direct analysis tool is more appropriate.

Mitigation: Confirm that the request contains a toxicant-disease or toxicant-phenotype pair and use a data-execution tool when the user needs live database queries, downloads, or analysis execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/aipoch-ai/skills/network-tox-docking-research-planner-1)
- [Decision Logic](references/decision-logic.md)
- [Study Patterns](references/study-patterns.md)
- [Workload Configurations](references/configurations.md)
- [Analysis Modules and Method Library](references/modules.md)
- [Mandatory Output Structure](references/output-standard.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown research plan with tables and structured sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs four workload configurations, a recommended primary plan, step-by-step workflow, figure plan, validation strategy, minimal executable version, and publication upgrade path.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
