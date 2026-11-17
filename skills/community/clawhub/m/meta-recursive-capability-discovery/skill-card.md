## Description:

This skill helps agents compare task requirements with an existing skill registry, identify recursive capability gaps and blind spots, and record local learning notes for later review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qq435912743](https://clawhub.ai/user/qq435912743)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to analyze whether an agent has the capabilities needed for an open-ended goal, find buildable capability gaps, and inspect blind spots before extending a skill set.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documentation describes broader autonomous self-improvement than the artifact actually implements.

Mitigation: Treat the skill as local capability-gap analysis with optional learning logs, and verify results against the provided registry and goal inputs.

Risk: The learner script can persist local notes in learned_patterns.json.

Mitigation: Review local learning records before sharing the skill directory and avoid recording secrets or sensitive task details.

Risk: Discovery quality depends on complete registry, requirement, decomposition, and dimension tag inputs.

Mitigation: Provide explicit capability tags and review leaf gaps and blind spots before using the output to prioritize new capabilities.

## Reference(s):

- [Skill definition](artifact/SKILL.md)
- [Distillation report](artifact/distillation_report.md)
- [ClawHub skill page](https://clawhub.ai/qq435912743/skills/meta-recursive-capability-discovery)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance and JSON results from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The local learner can create or update learned_patterns.json when outcome recording is used.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
