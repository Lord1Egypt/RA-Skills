## Description:

Provides an MBTI personality-test workflow intended to help an agent guide users through questions and report a Myers-Briggs type, while the packaged skill instructions remain incomplete.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettermen](https://clawhub.ai/user/bettermen)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill with an agent to run an MBTI-style questionnaire and receive a personality-type summary. Reviewers should confirm or complete the packaged workflow before relying on it because the artifact still contains placeholder instructions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact still contains placeholder instructions, so the agent may not run a reliable MBTI workflow.

Mitigation: Complete and review the trigger conditions, questionnaire flow, scoring approach, and result guidance before deployment.

Risk: Personality-test results can be overinterpreted by users.

Mitigation: Present results as informal self-reflection guidance rather than clinical, hiring, or other high-stakes assessment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bettermen/skills/mbti-test)
- [Reference Documentation for Mbti Test](references/api_reference.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown or plain text questionnaire results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include an MBTI type, answer-driven interpretation, and follow-up guidance after the workflow is completed.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
