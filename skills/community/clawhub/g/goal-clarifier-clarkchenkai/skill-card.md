## Description:

Goal Clarifier turns vague, solution-shaped requests into executable briefs by clarifying the goal, constraints, success criteria, scope, ambiguities, and next step before design or execution begins.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clarkchenkai](https://clawhub.ai/user/clarkchenkai)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agent operators use this skill to clarify vague requests before planning or implementation. It produces a structured brief that captures the intended outcome, constraints, success criteria, scope boundary, key ambiguities, and smallest safe next step.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad implicit activation can slow vague requests by asking clarifying questions before proposing a solution.

Mitigation: Use narrower trigger settings when users prefer explicit activation, or answer the missing goal, constraint, and success-criteria questions directly.

Risk: High-stakes or irreversible requests can be mishandled if vague goals are treated as ready for execution.

Mitigation: Require concrete success criteria, make the human decision boundary explicit, and keep execution planning out of the clarified brief until the purpose is clear.

## Reference(s):

- [Goal Clarifier Skill Page](https://clawhub.ai/clarkchenkai/skills/goal-clarifier-clarkchenkai)
- [Aristotle Reference](references/aristotle.md)
- [High-Risk Signals](references/high-risk.md)
- [Question Patterns](references/patterns.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown brief with six fixed headings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces targeted clarifying questions when required before emitting the final brief.]

## Skill Version(s):

1.0.0 (source: server release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
