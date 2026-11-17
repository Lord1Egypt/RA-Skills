## Description:

Improve Skill Bespoke To CodeBase is a meta-skill that evaluates Factory Droid skills against the current project and produces concrete, prioritized improvement recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[somacosf](https://clawhub.ai/user/somacosf)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to review an existing Factory Droid skill against the active codebase, identify gaps in clarity, edge case handling, output quality, composability, and user experience, and receive prioritized improvement recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can inspect projects and other skills, which may expose broad codebase context to the agent.

Mitigation: Invoke it with explicit target skill names and confirm the intended project and skill directory before review.

Risk: The skill can propose or apply changes to other skills' agent instructions, which could introduce incorrect or overly broad behavior.

Mitigation: Require a visible diff, review proposed SKILL.md and supporting-file changes before applying them, and keep a rollback path.

Risk: Broad triggers and limited scoping safeguards may cause the skill to run when the target skill is ambiguous.

Mitigation: Use explicit invocation for normal operation and ask for clarification whenever the target skill is not clear.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/somacosf/skills/improve-skill)
- [ClawHub publisher profile](https://clawhub.ai/user/somacosf)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown improvement report with scorecard, prioritized recommendations, edge case findings, and suggested SKILL.md patches]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include proposed edits for SKILL.md and supporting files after user approval.]

## Skill Version(s):

0.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
