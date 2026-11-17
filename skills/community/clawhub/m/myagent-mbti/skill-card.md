## Description:

Claw Mbti generates a playful MBTI-style personality report by analyzing a user's recent natural-language interactions with OpenClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaoyang0807](https://clawhub.ai/user/xiaoyang0807)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users use this skill to request a playful MBTI-style report based on recent conversation behavior. The skill also provides no-data and low-data responses when there is not enough interaction history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks to analyze recent conversation history and memory, which can reveal private behavioral patterns.

Mitigation: Run it only with clear user intent, and avoid sharing generated reports when they expose sensitive personal patterns.

Risk: Generated personality reports may be misleading if treated as a formal psychological assessment.

Mitigation: Present results as playful, non-clinical impressions and review outputs before relying on them.

Risk: The skill can show GitHub install or update commands that modify a local OpenClaw skills directory.

Mitigation: Run installation commands only intentionally after confirming the repository and target directory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiaoyang0807/skills/myagent-mbti)
- [Project homepage](https://github.com/xiaoyang0807/claw-mbti)
- [MBTI diagnosis reference](artifact/reference.md)
- [Lobster MBTI type catalog](artifact/types.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Shell commands]

**Output Format:** [Markdown report with tables and inline shell commands for installation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses recent natural-language conversation history when available; falls back to no-data or low-data responses.]

## Skill Version(s):

1.5.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
