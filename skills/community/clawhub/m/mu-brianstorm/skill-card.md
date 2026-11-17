## Description:

Brainstorm guides Chinese-language planning conversations that turn fuzzy ideas into actionable design plans.

This skill is ready for commercial/non-commercial use.

## Publisher:

[caspermoo](https://clawhub.ai/user/caspermoo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and product teams use Brainstorm to clarify ambiguous ideas, compare implementation paths, and produce structured design plans for new features or technical decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can produce design plans that include private product or architecture details.

Mitigation: Review generated plans before committing or sharing them, and avoid including sensitive details unless the repository is approved for that information.

Risk: The skill may create files under docs/plans or suggest git commits as part of the planning workflow.

Mitigation: Require user confirmation before creating planning files or running git commit.

Risk: Brainstorming output can be incomplete or misleading if early assumptions are wrong.

Mitigation: Use the skill's staged confirmation steps to verify goals, constraints, selected approach, and final design before implementation.

## Reference(s):

- [Design Patterns](references/design-patterns.md)
- [Output Templates](references/output-templates.md)
- [Question Templates](references/question-templates.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands]

**Output Format:** [Markdown conversation guidance and design document templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create a design plan under docs/plans after the user confirms the design direction.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
