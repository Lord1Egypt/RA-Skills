## Description:

Chain tasks into sequential pipelines across agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to build multi-step workflows across specialized agents, passing each completed result into the next dependent task.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Intermediate task results may contain secrets, personal data, or proprietary content.

Mitigation: Review and redact intermediate results before passing them to other agents or endpoints.

Risk: Chained workflows may send task results to agents or endpoints outside the user's trust boundary.

Mitigation: Use the skill only with trusted agents and intended pilotctl workflows.

## Reference(s):

- [Pilot Protocol](https://pilotprotocol.network)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include sequential task instructions that pass intermediate results between agents.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
