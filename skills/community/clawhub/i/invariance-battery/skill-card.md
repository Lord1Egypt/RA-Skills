## Description:

Runtime assertion system that continuously verifies AI agent invariants - properties that must always hold.

This skill is ready for commercial/non-commercial use.

## Publisher:

[evezart](https://clawhub.ai/user/evezart)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to define runtime invariant checks for autonomous agents, detect drift from intended behavior, and frame falsification reports when an invariant fails.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An implemented invariant gate could block actions or create logs in ways that exceed the intended scope.

Mitigation: Explicitly scope checked actions, halt behavior, audit log contents, and retention policy before deployment.

Risk: Invariant guidance can be misapplied if checks are treated as proof that an agent is correct.

Mitigation: Use invariant failures as falsification signals and review proposed checks before operational use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/evezart/skills/invariance-battery)

## Skill Output:

**Output Type(s):** [guidance, markdown, code]

**Output Format:** [Markdown guidance with Python code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Conceptual guidance only; no executable hooks, credential use, or hidden behavior were identified in the supplied security evidence.]

## Skill Version(s):

1.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
