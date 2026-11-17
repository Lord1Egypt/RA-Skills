## Description:

Generates structured PRDs and requirements review checklists from a short Chinese or English requirement, with optional UML diagrams, JSON export, and multi-role review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shylamb-token](https://clawhub.ai/user/shylamb-token)

### License/Terms of Use:

MIT-0

## Use Case:

Product managers, developers, QA reviewers, and product teams use this skill to expand concise requirements into structured PRDs, acceptance-oriented review checklists, and optional exports for downstream planning tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated PRDs may contain confidential roadmap, customer, security, or business details.

Mitigation: Review generated content before sharing or exporting it, and avoid including sensitive details unless the workspace and recipients are appropriate.

Risk: Optional file and JSON exports may place product-planning information where downstream tools or CI systems can consume it.

Mitigation: Choose export filenames and locations deliberately, and review exported files before connecting them to Notion, Jira, CI, or similar systems.

Risk: Short or ambiguous requirements can lead to speculative PRD assumptions.

Mitigation: Use the skill's clarification step for vague inputs and review assumptions, external dependencies, compliance notes, and acceptance criteria before implementation planning.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shylamb-token/skills/prd-autogen-and-review)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Code, Guidance, Configuration]

**Output Format:** [Markdown PRD and checklist, with optional SVG/HTML diagram and JSON export]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write user-directed PRD Markdown or JSON files when export is requested.]

## Skill Version(s):

1.5.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
