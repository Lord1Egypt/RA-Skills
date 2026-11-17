## Description:

Teaches any topic in adaptive sessions: probes prior knowledge, calibrates depth and format, and checks retention before advancing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

External learners and agents use this skill for adaptive tutoring sessions across topics, including diagnostic probes, explanations, worked examples, retrieval checks, misconception repair, and retention-oriented review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local learning history and preferences may retain sensitive study context.

Mitigation: Review or delete files under ~/Clawic/data/learning/ if retained learning history is not desired.

Risk: Shared language or locale defaults may be read from ~/Clawic/profile.yaml.

Mitigation: Review that local profile before use if shared defaults should not influence tutoring sessions.

Risk: Text-only tutoring cannot fully validate speaking, listening, or motor-skill practice.

Mitigation: Use the skill for theory and planning, then route real practice to the appropriate activity, tool, or coach.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/learning)
- [Clawic skill page](https://clawic.com/skills/learning)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Conversational Markdown with teaching prompts, worked examples, retrieval checks, and optional local learning notes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local learning preference and topic-progress files under ~/Clawic/data/learning/.]

## Skill Version(s):

1.0.3 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
