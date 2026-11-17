## Description:

Guides agents through a confirmed 7-step Chinese-language workflow for creating PRDs, prototypes, user stories, flows, ER models, RBAC matrices, and tracking plans for company-internal process systems.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lailiai](https://clawhub.ai/user/lailiai)

### License/Terms of Use:

MIT-0

## Use Case:

Product managers and internal-tools teams use this skill to structure a new company-internal process system from early input collection through PRD and prototype delivery. It emphasizes role-aware workflows, user confirmation checkpoints, RBAC, tracking plans, and traceable decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated PRDs, RBAC rules, tracking events, and prototypes may contain assumptions that are not suitable for a real internal system.

Mitigation: Keep the documented checkpoint flow and require product, security, and data-owner review before using outputs as implementation plans.

Risk: Tracking examples can involve employee or payroll-related data and may create privacy or compliance concerns.

Mitigation: Review analytics events and properties for minimization, access control, retention, and local privacy requirements before adoption.

Risk: The packaged skill references some step files under a path that differs from the included artifact layout.

Mitigation: Confirm referenced files resolve in the target agent environment before release or update the references to match the packaged paths.

## Reference(s):

- [Input Collection](references/step2-input-collection.md)
- [Validation Checks](references/step3-validation.md)
- [User Stories](references/step4-user-stories.md)
- [Flows and State Machines](references/step5-flows.md)
- [Modules and ER Model](references/step6-modules-er.md)
- [RBAC and Tracking Plan](references/step6.5-rbac-tracking.md)
- [Prototype and PRD Output](references/step7-output.md)
- [Self-check Checklist](references/selfcheck.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown documents, Mermaid diagrams, HTML prototype code, structured tables, and concise guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces staged artifacts with user confirmation checkpoints before downstream work continues.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
