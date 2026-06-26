## Description: <br>
Guides Chinese-language product teams through a checkpointed workflow for designing company-internal process management PRDs, prototypes, user stories, flows, ER models, RBAC matrices, tracking plans, and final PRD deliverables. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lailiai](https://clawhub.ai/user/lailiai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Product managers, business analysts, and internal platform teams use this skill to structure a new company-internal workflow system from initial requirements through validated PRD and prototype outputs. It is intended for internal process-management products where roles, approvals, state changes, data permissions, and tracking events must be explicit. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may include payroll records, secrets, or unnecessary employee identifiers while drafting internal-system examples. <br>
Mitigation: Use synthetic or minimized data in prompts and examples; exclude secrets and unnecessary employee identifiers. <br>
Risk: Generated RBAC and tracking plans may imply collection or access patterns that need privacy, retention, and compliance review. <br>
Mitigation: Review generated permissions, event properties, retention expectations, and access controls with legal, privacy, security, and business stakeholders before implementation. <br>
Risk: A generated PRD or prototype may omit edge cases or encode unconfirmed product assumptions. <br>
Mitigation: Use the skill's checkpoint and self-check workflow to confirm assumptions, mark unresolved items with TODOs, and require stakeholder approval before downstream technical design. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/lailiai/prdwriter) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [Step 2 input collection](artifact/references/step2-input-collection.md) <br>
- [Step 3 validation](artifact/references/step3-validation.md) <br>
- [Step 4 user stories](artifact/references/step4-user-stories.md) <br>
- [Step 5 flows](artifact/references/step5-flows.md) <br>
- [Step 6 modules and ER model](artifact/references/step6-modules-er.md) <br>
- [Step 6.5 RBAC and tracking](artifact/references/step6.5-rbac-tracking.md) <br>
- [Step 7 output](artifact/references/step7-output.md) <br>
- [Self-check checklist](artifact/references/selfcheck.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown documents, Mermaid diagrams, tabular specifications, and single-file HTML prototype code] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces checkpointed PRD artifacts and prototype guidance; generated outputs should be reviewed before implementation.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
