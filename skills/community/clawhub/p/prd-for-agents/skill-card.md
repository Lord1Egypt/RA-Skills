## Description:

Use this skill when an agent or user needs to write, draft, create, or review a PRD, product requirements document, product spec, or feature spec for AI coding agents, developer agents, or multi-agent pipelines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sanketsao](https://clawhub.ai/user/sanketsao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, product managers, founders, and agent operators use this skill to turn an idea or existing draft into a structured PRD that an AI builder or developer agent can execute. It is intended for PRD creation, completeness review, and handoff readiness checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill has broad activation around requirements and spec-writing prompts, which may produce a full PRD when the user only wanted lightweight brainstorming.

Mitigation: Use explicit wording when requesting informal ideation, and reserve PRD-related phrasing for cases where a structured handoff document is desired.

Risk: A generated PRD may contain unresolved assumptions or open questions that could affect scope before an agent begins implementation.

Mitigation: Review the assumptions, open questions, and handoff readiness checklist before routing the PRD to a builder or developer agent.

## Reference(s):

- [PRD Sections Reference](references/prd-sections.md)
- [PRD Examples Reference](references/prd-examples.md)
- [ClawHub Skill Page](https://clawhub.ai/sanketsao/skills/prd-for-agents)
- [Publisher Profile](https://clawhub.ai/user/sanketsao)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown PRD with structured sections, tables, checklists, and handoff guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a sequenced PRD structure with user stories, acceptance criteria, metrics, dependencies, risks, assumptions, open questions, and agent build order.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
