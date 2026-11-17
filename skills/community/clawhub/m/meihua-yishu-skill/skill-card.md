## Description:

梅花易数排盘与断卦技能，支持数字起卦、时间起卦、方位起卦，并生成互卦、变卦、体用分析和自动化断卦结果。

This skill is ready for commercial/non-commercial use.

## Publisher:

[dglijin-oss](https://clawhub.ai/user/dglijin-oss)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run a local Chinese-language Mei Hua Yi Shu divination CLI, generate hexagram readings from numbers, time, direction, or random input, and review formatted or JSON results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Saved reading history can retain sensitive health, relationship, finance, investment, travel, dispute, or personal question details on the local filesystem.

Mitigation: Avoid using --save for sensitive questions, or periodically review and delete the local guali history files when retention is not needed.

Risk: Divination-style outputs may be mistaken for authoritative advice in health, finance, legal, or dispute contexts.

Mitigation: Treat readings as cultural or reflective guidance and consult qualified professionals before making consequential decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dglijin-oss/skills/meihua-yishu-skill)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Plain text or JSON emitted by a local Python CLI, with example shell commands in the skill documentation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Optional --save writes reading records and an index to a local guali directory.]

## Skill Version(s):

3.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
