## Description:

提供专业六爻预测功能，进行中国传统易学占卜，支持起卦、排盘、纳甲、寻世应、定六亲、配六神及吉凶判断。

This skill is ready for commercial/non-commercial use.

## Publisher:

[qichenx](https://clawhub.ai/user/qichenx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to generate Liuyao divination charts and receive structured Chinese-language explanations of hexagrams, changing lines, relationships, spirits, void branches, and fortune judgments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may include unnecessary sensitive personal details in divination questions.

Mitigation: Ask only for the minimum question context and sex parameter needed for the reading, and avoid collecting identifying details.

Risk: The optional project-integrated flow depends on trusted surrounding project modules and uses an unsafe import pattern.

Mitigation: Prefer the standalone liuyao_standalone.py flow; use liuyao_skill.py only in a trusted project directory.

Risk: Divination output may be mistaken for factual, medical, legal, or financial advice.

Mitigation: Present results as traditional Liuyao interpretation and route high-stakes decisions to appropriate qualified advice.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qichenx/skills/liuyao-divination)
- [GitHub repository listed in skill documentation](https://github.com/QiChenX/LiuYaoDivining)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Chinese-language Markdown or structured text with optional JSON-like Python dictionaries from the standalone module.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local divination results from a user question and optional sex parameter; no network service is required by the recommended standalone flow.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
