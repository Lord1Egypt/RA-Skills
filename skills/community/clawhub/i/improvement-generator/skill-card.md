## Description:

Generates ranked improvement candidates for skills from target analysis, feedback sources, and failure traces.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lanyasheng](https://clawhub.ai/user/lanyasheng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to generate structured improvement candidates for skills before those candidates are scored, approved, or executed. It can incorporate memory, feedback, and previous failure traces to adjust candidate priorities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Target skill content may be sent to an external Claude CLI during candidate generation.

Mitigation: Use non-sensitive targets unless external processing is explicitly approved, and review target content before running the skill.

Risk: Generated file-change plans may not be contained to the target skill.

Mitigation: Require downstream path containment checks, action allowlisting, and human approval before applying generated candidates.

Risk: Generated proposals may be incorrect or misleading.

Mitigation: Review and scan candidates before deployment, and route them through scoring or evaluation before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lanyasheng/skills/improvement-generator)

## Skill Output:

**Output Type(s):** [Guidance, Code, Configuration]

**Output Format:** [JSON containing ranked improvement candidates and execution plans]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Candidates include category, risk_level, execution_plan, priority signals, and trace adjustment metadata when available.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
