## Description:

A meta-skill distilled from self-play-coevolution that adds self-verification, reflection, super-agent orchestration, and continuous self-evolution loops to improve coevolution workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qq435912743](https://clawhub.ai/user/qq435912743)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent users use this skill to perform self-play coevolution tasks with added verification, reflection, and learning loops. It is intended to make coevolution outputs more traceable while recording local learning patterns for later iterations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill documentation promises broader autonomous capabilities than the artifact clearly implements.

Mitigation: Review generated guidance and require explicit human approval before treating claims of self-verification, orchestration, or self-evolution as operational controls.

Risk: The learner script stores arbitrary local notes across sessions, which could influence later agent behavior without clear controls.

Mitigation: Inspect and prune local learned_patterns.json state before reuse, and avoid storing sensitive or unreviewed instructions in learner notes.

## Reference(s):

- [Distillation report](artifact/distillation_report.md)
- [ClawHub skill page](https://clawhub.ai/qq435912743/skills/meta-self-play-coevolution)
- [Publisher profile](https://clawhub.ai/user/qq435912743)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with optional JSON learner records and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local learned_patterns.json state when learner.py is invoked.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
