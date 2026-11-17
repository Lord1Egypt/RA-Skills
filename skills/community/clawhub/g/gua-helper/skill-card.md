## Description:

梅花易数起卦，根据上卦、下卦数字查六十四卦，给出卦名、动爻及详解链接。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaobo1992](https://clawhub.ai/user/xiaobo1992)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this Chinese-language skill to calculate a Meihua I Ching hexagram from upper and lower trigram numbers and receive a concise interpretive reading with a detail link.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Divination output may be mistaken for factual, financial, legal, medical, or safety-critical advice.

Mitigation: Present readings as interpretive entertainment or cultural guidance and require users to make consequential decisions using appropriate professional sources.

Risk: Results vary with the current time and normalize inputs modulo 8, so users may see unexpected results for large numeric inputs or repeated runs at different times.

Mitigation: Explain the time-dependent calculation and modulo normalization when users ask how a result was produced.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiaobo1992/skills/gua-helper)
- [Publisher profile](https://clawhub.ai/user/xiaobo1992)
- [八卦对照表](references/bagua.md)
- [十二时辰与时序对照表](references/shichen.md)
- [六十四卦速查表](assets/64gua_table.md)
- [卦意链接映射](references/guas.json)
- [周易卦意参考](https://www.zhouyi.cc/zhouyi/yijing64/4103.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown text with calculated hexagram fields and a short Chinese interpretation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output depends on current local time and normalizes numeric inputs modulo 8.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
