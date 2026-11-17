## Description:

Generates structured, publication-oriented research designs for non-tumor biomedical machine learning studies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to plan non-cancer bioinformatics and machine learning studies, including diagnostic biomarker designs, GEO dataset workflows, mechanism-focused analyses, validation plans, and publication-tier workload options.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad biomedical ML planning prompts may activate the skill outside the intended non-cancer research-planning scope.

Mitigation: Ask users to provide a clear non-cancer disease, mechanism, or diagnostic-biomarker goal before generating a plan.

Risk: Generated study plans may depend on suitable GEO or public datasets that have not yet been confirmed.

Mitigation: When dataset availability is uncertain, provide a dataset search guide and mark the plan as tentative until data suitability is confirmed.

Risk: Research plans can overstate diagnostic or mechanistic conclusions if validation limits are ignored.

Mitigation: Require explicit separation of feature-discovery, model, clinical utility, biological support, and external-validation evidence layers.

## Reference(s):

- [Workload Configuration Reference](references/configurations.md)
- [Modules and Methods Reference](references/modules-and-methods.md)
- [Study Patterns Reference](references/study-patterns.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Configuration instructions]

**Output Format:** [Structured Markdown research plan]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Planning-only output; no executable code, persistence, credential use, or hidden data handling observed in the security evidence.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
