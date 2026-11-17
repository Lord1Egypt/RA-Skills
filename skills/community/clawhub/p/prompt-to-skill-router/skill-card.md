## Description:

Route each request to the best execution path: direct answer, installed skill, new skill, or a multi-skill workflow, with explicit reasoning about friction, value, and fit.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobewin](https://clawhub.ai/user/tobewin)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use this skill to decide whether a request should be handled directly, with an installed skill, with a new skill, or through a multi-skill workflow. It is intended for routing decisions where friction, value, fit, and route alternatives need to be stated clearly.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may cause agents to discuss routing more often than users expect.

Mitigation: Use narrow activation wording and prefer a direct answer when the best path is already clear.

Risk: A routing recommendation could add unnecessary complexity for a simple request.

Mitigation: Apply the skill's friction-versus-value check and choose the lowest-friction route that can produce a good result.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/tobewin/skills/prompt-to-skill-router)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Text]

**Output Format:** [Markdown route assessment with a best route, next step, comparison against alternatives, and optional skill path.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces decision-support prose only; it does not execute code, call external systems, or access data.]

## Skill Version(s):

1.0.0 (source: release evidence and artifact metadata.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
