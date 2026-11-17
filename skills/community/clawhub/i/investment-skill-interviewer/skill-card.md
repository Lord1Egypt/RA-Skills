## Description:

投研Skill面试官--对金融投研类skill进行全面结构化评估，按七维度打分并输出综合评分报告。用于在众多投研skill中做选型决策。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenxyzcyxpp](https://clawhub.ai/user/chenxyzcyxpp)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to evaluate China/A-share-oriented investment research skills, score them across seven dimensions, and produce a structured selection report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to actually run evaluated skills without specifying sandboxing, approval, or capability limits.

Mitigation: Run target skills only in a disposable, least-privilege sandbox with no host secrets or broad filesystem access, and treat dynamic validation as optional unless the requested capabilities are explicitly approved.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown evaluation report with scoring tables and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language report; may include compliance prescreening, seven-dimension scores, detailed comments, prioritized improvements, and multi-skill comparison.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
