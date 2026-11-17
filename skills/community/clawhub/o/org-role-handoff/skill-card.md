## Description:

Take on roles from the target organization's IT and operational structure and respond from that role's perspective, responsibilities, scope, boundaries, collaboration context, and expected output style.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nalendrax8](https://clawhub.ai/user/nalendrax8)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and developers use this skill when they want an agent to answer from a specific organizational role such as Executive Director, IT Director, Quality Assurance, Database Administrator, Web Developer, Product & Project Manager, UI/UX Designer, Business Analyst, or General Administration. It helps structure role-specific recommendations, checklists, reviews, implementation plans, validation plans, coordination briefs, and handoffs while preserving role boundaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Ambiguous shorthand such as PM, BA, QA, admin, developer, or designer can cause the agent to answer from an unintended role perspective.

Mitigation: Ask a brief clarification when ambiguity would materially change the answer, or state the assumed role when speed is preferred.

Risk: Role-based framing can overstate a role's authority or blur ownership across business, design, operations, and technical responsibilities.

Mitigation: Use the role-boundary and collaboration references to answer from the requested role first, then identify adjacent roles needed for decisions or follow-up.

## Reference(s):

- [Skill page](https://clawhub.ai/nalendrax8/skills/org-role-handoff)
- [Organization Context](references/org-context.md)
- [Role Definitions](references/role-definitions.md)
- [Role Synonyms](references/role-synonyms.md)
- [Role Selection Rules](references/role-selection-rules.md)
- [Role Boundaries](references/role-boundaries.md)
- [Collaboration Rules](references/collaboration-rules.md)
- [Handoff Patterns](references/handoff-patterns.md)
- [Output Modes](references/output-modes.md)
- [Default Response Shape](references/default-response-shape.md)
- [Anti-Patterns](references/anti-patterns.md)
- [Multi-Role Response Rules](references/multi-role-response-rules.md)
- [Examples](references/examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text shaped to the requested organizational role and task]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use role brief, checklist, recommendation, or task-output templates when those structures fit the request.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
