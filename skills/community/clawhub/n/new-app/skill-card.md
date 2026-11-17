## Description:

Use when creating a new internal application from scratch, standardizing a 0-to-1 app build workflow, or helping teammates bootstrap a Next.js/FastAPI/Keycloak/PostgreSQL style product with a docs-first process.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lyc-chengzi](https://clawhub.ai/user/lyc-chengzi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and internal product teams use this skill to turn a new app idea into a documented, reviewable MVP plan before implementation. It guides requirements clarification, architecture selection, documentation updates, toolchain setup, thin-slice implementation, and validation for internal full-stack applications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Architecture or implementation guidance could be wrong if the business problem, access model, data sensitivity, or MVP boundary is not confirmed first.

Mitigation: Use the requirements templates, confirm constraints and architecture before coding, and keep documentation aligned with the implementation.

Risk: Auth, database, storage, upload, or deployment choices may introduce security or operational gaps when copied without local review.

Mitigation: Review secret handling, identity boundaries, schema migration plans, diagnostics, and validation results before treating a generated app as ready.

## Reference(s):

- [Internal App Requirements Template](templates/requirements-template.md)
- [Internal App Requirements Template (Chinese)](templates/requirements-template.cn.md)
- [Internal App Delivery Checklist](templates/delivery-checklist.md)
- [Internal App Delivery Checklist (Chinese)](templates/delivery-checklist.cn.md)
- [ClawHub Skill Page](https://clawhub.ai/lyc-chengzi/skills/new-app)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with implementation plans, code and configuration changes, shell commands, validation results, and follow-up recommendations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce bilingual documentation updates and reusable requirements or delivery checklist content.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
