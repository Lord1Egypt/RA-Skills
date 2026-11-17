## Description:

Architecture thinking training that uses guided questioning to teach users how to reason from a PRD to architecture decisions instead of directly producing an architecture for them.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phy041](https://clawhub.ai/user/phy041)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and product builders use this skill to practice architecture reasoning for real project or PRD scenarios through Socratic prompts, tradeoff analysis, component decomposition, interface choices, data design, failure planning, and ADR writing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger phrases may activate the skill when the user did not intend to start architecture coaching.

Mitigation: Use the explicit /architect-mentor command for predictable activation and disable or avoid broad trigger phrasing when working in unrelated contexts.

Risk: Architecture coaching can shape technical decisions, and users may over-apply generated prompts or examples without validating them against project constraints.

Mitigation: Review resulting diagrams, ADRs, quality-attribute priorities, and tradeoffs with project stakeholders before using them for implementation decisions.

## Reference(s):

- [Canlah AI homepage](https://canlah.ai)
- [ClawHub skill page](https://clawhub.ai/phy041/skills/phy-architect-mentor)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown conversational coaching with questions, explanations, checklists, diagrams, and ADR examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces instructional architecture coaching and structured reasoning artifacts such as context diagrams, component diagrams, data models, ADRs, and quality-attribute priorities.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
