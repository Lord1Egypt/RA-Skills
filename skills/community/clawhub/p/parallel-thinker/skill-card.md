## Description:

Parallelize queries across multiple specialized agents and synthesize their responses into a unified answer.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liyico](https://clawhub.ai/user/liyico)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to get faster, multi-perspective analysis for complex questions by consulting several specialized local agents and consolidating their responses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can invoke caller-selected local agents without the limits its documentation claims.

Mitigation: Use only with trusted callers and non-privileged local agents; add an allowlist, timeouts, output limits, and enforced concurrency limits before shared or sensitive deployment.

Risk: Queries and intermediate expert responses may expose sensitive context across multiple agents.

Mitigation: Avoid sending secrets or regulated data, and review synthesized answers before relying on them for consequential decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/liyico/skills/parallel-thinker)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [JSON containing a synthesized response and per-agent responses, typically returned to the agent as text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes available expert responses and error messages for failed agent calls.]

## Skill Version(s):

1.0.0 (source: release metadata and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
