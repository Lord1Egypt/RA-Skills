## Description:

Routes product design requests to workflows for new internal process systems, product iterations, and SaaS productization, producing PRDs and interactive prototypes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lailiai](https://clawhub.ai/user/lailiai)

### License/Terms of Use:

MIT-0

## Use Case:

Product managers, founders, and internal-tool teams use this skill to turn product design requests into structured PRDs, user stories, workflows, RBAC and tracking plans, and high-fidelity prototypes for internal process systems or SaaS productization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may save or transform sensitive product materials such as screenshots, HTML prototypes, DDL, internal URLs, credentials, or confidential business context.

Mitigation: Use only sanitized materials, redact personal data and secrets before invoking the skill, and review generated files before sharing or deployment.

Risk: Generated or template-based prototypes may run unpinned third-party CDN scripts.

Mitigation: Avoid opening prototypes in a sensitive browser context unless dependencies are pinned, integrity-protected, or vendored locally.

Risk: The scanner verdict is suspicious because the skill stores potentially sensitive internal materials and generates executable prototypes.

Mitigation: Review the skill before installing, follow the scanner guidance, and scan generated prototypes before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lailiai/skills/prd-design)
- [Product Design Router](artifact/SKILL.md)
- [Product Design 0to1 Workflow](artifact/0to1/SKILL0to1.md)
- [Product Design Iteration Workflow](artifact/iteration/SKILLiteration.md)
- [SaaS Productization Workflow](artifact/productization/SKILLproductization.md)
- [Prototype and PRD Output Rules](artifact/shared/steps/step7-output.md)
- [Iteration Prototype Template](artifact/iteration/references/templates/prototype-template.html)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown PRDs and single-file HTML prototypes with supporting design guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate project files for inputs, flows, RBAC, tracking plans, PRDs, and prototypes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
