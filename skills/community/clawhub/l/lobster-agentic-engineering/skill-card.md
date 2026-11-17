## Description:

Operate as an agentic engineer using eval-first execution, decomposition, and cost-aware model routing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangxiaofei860208-source](https://clawhub.ai/user/wangxiaofei860208-source)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to guide agent-led implementation work with upfront completion criteria, small independently verifiable task units, eval-first feedback loops, cost-aware model routing, and focused review of AI-generated code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can influence how an agent plans engineering work, chooses model tiers, and prioritizes review.

Mitigation: Treat its recommendations as process guidance and keep human review over task decomposition, model escalation, and quality gates.

Risk: Eval or regression criteria chosen too narrowly may miss defects in AI-generated implementation work.

Mitigation: Define completion criteria before execution, run baseline and post-change evals, and review invariants, edge cases, security assumptions, and rollout risk.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangxiaofei860208-source/skills/lobster-agentic-engineering)
- [Publisher profile](https://clawhub.ai/user/wangxiaofei860208-source)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown guidance and concise engineering workflow recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill provides process guidance and does not add code execution, persistence, credential access, or data-access behavior by itself.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
