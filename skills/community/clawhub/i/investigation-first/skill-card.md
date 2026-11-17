## Description:

Trigger before making claims or decisions when context is incomplete, evidence is weak, or the domain is unfamiliar; use this skill to investigate first, gather firsthand facts, and let reality shape the conclusion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arg0](https://clawhub.ai/user/arg0)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill before recommendations, decisions, or claims when facts, context, or firsthand evidence are incomplete. It guides systematic investigation, evidence recording, uncertainty marking, and conclusion-writing grounded in observed facts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill encourages broad fact gathering, including reading code, logs, git history, and running tests.

Mitigation: Set clear investigation scope and avoid directing the agent at sensitive logs or private repositories unless that access is intended.

## Reference(s):

- [Investigation First skill page](https://clawhub.ai/arg0/skills/investigation-first)
- [Original source excerpts](original-texts.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, shell commands]

**Output Format:** [Markdown guidance and structured investigation reports, with shell commands when evidence gathering requires direct checks.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Encourages separating confirmed facts, reasonable inferences, unresolved questions, conclusions, and recommendations.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
