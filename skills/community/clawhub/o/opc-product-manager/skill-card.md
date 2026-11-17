## Description:

OPC Product Manager turns a one-sentence product idea for a solo entrepreneur into a build-ready specification with MVP scope, tech stack recommendations, complexity assessment, and agent handoff guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leonfjr](https://clawhub.ai/user/leonfjr)

### License/Terms of Use:

MIT-0

## Use Case:

External users, especially solo entrepreneurs and one-person company operators, use this skill to turn product ideas into build-ready specifications for AI coding agents. It supports full specs, quick specs, scope checks, tech stack recommendations, spec reviews, handoff documents, and product status summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create and update local products/ files and index metadata.

Mitigation: Use it in a project-scoped workspace and review generated or modified files before relying on them.

Risk: Generated specs can include build commands and technical recommendations that may be incorrect or unsuitable for the project.

Mitigation: Review build commands, dependencies, architecture choices, and acceptance criteria before running commands or assigning implementation work.

Risk: The skill may use contract or invoice context if those lookups are allowed.

Mitigation: Allow contract or invoice lookups only when that business data is intended to inform the product specification.

## Reference(s):

- [Tech Stack Guide](references/tech-stack-guide.md)
- [User Story Patterns](references/user-story-patterns.md)
- [Scope Assessment](references/scope-assessment.md)
- [Product Spec Template](templates/product-spec.md)
- [Quick Spec Template](templates/quick-spec.md)
- [Handoff Spec Template](templates/handoff-spec.md)
- [Product Metadata Schema](templates/product-metadata-schema.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code blocks and optional JSON metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local product specification files, handoff files, and product index metadata when archive workflows are used.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
