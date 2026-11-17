## Description:

Standardizes cross-agent communication protocols for asking another agent questions, collaborating, or delegating tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[auberghan](https://clawhub.ai/user/auberghan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators of multi-agent systems use this skill to choose blocking, fire-and-forget, or background delegation patterns and format requests consistently.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agent-to-agent messages can forward unnecessary private or sensitive context.

Mitigation: Include only the context needed for the receiving agent to complete the request.

Risk: Background delegation can run longer tasks that affect important data or decisions.

Mitigation: Confirm long-running delegation before use when the result could materially affect data, users, or decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/auberghan/skills/openclaw-agent-comm)

## Skill Output:

**Output Type(s):** [guidance, markdown, text]

**Output Format:** [Markdown guidance with protocol templates and tool-call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes recommended timeout values and control directives for cross-agent communication.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
