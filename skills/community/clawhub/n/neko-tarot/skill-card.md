## Description:

引导 Agent 使用猫咪塔罗 CLI 推荐牌阵、执行数字抽牌或实体牌录入，并生成结合用户意图的中文塔罗解读提示。

This skill is ready for commercial/non-commercial use.

## Publisher:

[senzi](https://clawhub.ai/user/senzi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill to conduct Chinese-language tarot readings with structured spread selection, card drawing, card-to-position mapping, and prompt assembly. It supports both fully digital draws and companion mode for users with physical cards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tarot output could be mistaken for professional financial, medical, legal, or mental-health advice.

Mitigation: Present readings as reflective or entertainment-oriented guidance and direct users to qualified professionals for high-stakes decisions.

Risk: Unpinned Python dependencies can reduce installation reproducibility.

Mitigation: Install in a virtual environment and pin dependency versions when deploying or sharing the skill.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/senzi/skills/neko-tarot)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)
- [TAROT_DATA.md](artifact/TAROT_DATA.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Chinese prose guidance, Markdown instructions, shell command examples, and JSON CLI responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The CLI can list spreads, randomly draw cards, compose prompts from physical-card inputs, and return structured JSON for agent parsing.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
