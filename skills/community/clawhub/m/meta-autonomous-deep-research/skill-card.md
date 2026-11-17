## Description:

A Chinese-language research workflow skill that prompts an agent to decompose questions, retrieve evidence, synthesize findings, reflect on gaps, iterate, and optionally record simple learner notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qq435912743](https://clawhub.ai/user/qq435912743)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users can use this skill to guide Chinese-language deep research tasks through decomposition, evidence collection, synthesis, reflection, and iteration. It is best treated as a workflow prompt with a simple local learner log, not as a complete autonomous research system by itself.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill advertises self-verification, orchestration, and autonomous research behavior that may not exist without supporting tools.

Mitigation: Verify or add the supporting tools before relying on those behaviors, and review research outputs for evidence quality.

Risk: Learner notes are persisted locally and could expose sensitive task details if users record them.

Mitigation: Do not pass secrets, credentials, or sensitive research details into learner notes.

Risk: The distilled workflow may not capture all implicit behavior from the teacher skill.

Mitigation: Compare critical decisions against the original teacher skill or other trusted sources before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qq435912743/skills/meta-autonomous-deep-research)
- [Publisher profile](https://clawhub.ai/user/qq435912743)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Text, JSON]

**Output Format:** [Chinese-language Markdown guidance with optional JSON learner-log output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose research structure, confidence notes, follow-up retrieval steps, and learner-log entries.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
