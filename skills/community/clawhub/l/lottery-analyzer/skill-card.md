## Description:

彩票分析助手 analyzes China Double Color Ball and China Lotto draw data to summarize trends, identify hot and cold numbers, detect number patterns, and generate statistically based lottery number recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[larval-zz](https://clawhub.ai/user/larval-zz)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to analyze user-provided SSQ or DLT Excel/CSV draw data, review frequency and pattern statistics, and generate entertainment-only lottery number recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Lottery recommendations may be misunderstood as a guarantee or prediction of winning outcomes.

Mitigation: Treat all recommendations as entertainment-only statistical analysis; the skill states that lottery outcomes are random and does not guarantee winning.

Risk: The skill reads lottery data files supplied by the user.

Mitigation: Provide only intended Excel or CSV draw-history files and review the resulting analysis before relying on it.

Risk: The skill may save analysis reports locally under /home/admin/worktemp.

Mitigation: Inspect, retain, or remove generated report files according to local data-handling expectations.

## Reference(s):

- [ClawHub skill page: lottery-analyzer](https://clawhub.ai/larval-zz/skills/lottery-analyzer)
- [Publisher profile: larval-zz](https://clawhub.ai/user/larval-zz)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, JSON, guidance]

**Output Format:** [Markdown guidance with Python and shell examples; analysis reports are saved as JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads user-provided Excel or CSV lottery data and may save local reports under /home/admin/worktemp.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
