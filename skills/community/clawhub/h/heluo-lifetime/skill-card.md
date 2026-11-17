## Description:

河洛理数 · 一卦定终身 is a Chinese-language divination-style skill that uses birth date/time, approximate birthplace, and gender to calculate Heluo Lishu natal hexagrams, later-life hexagrams, major luck cycles, annual readings, and a Markdown lifetime reading.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leahlu0124-creator](https://clawhub.ai/user/leahlu0124-creator)

### License/Terms of Use:

MIT-0

## Use Case:

External Chinese-language users use this skill to generate a divination-style lifetime reading from birth details, including natal and later-life hexagrams, major luck cycles, annual readings, and follow-up plain-language explanations. Agents use it when a user asks for Heluo Lishu, lifetime-hexagram, major-cycle, or annual-fortune readings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to provide birth date/time, approximate birthplace, and gender.

Mitigation: Only provide details you are comfortable sharing, avoid unnecessary identifying context, and keep processing local where possible.

Risk: Divination-style outputs could be mistaken for factual life, career, health, or financial predictions.

Mitigation: Treat readings as entertainment and reflective guidance, not as the sole basis for consequential decisions.

Risk: The security evidence notes a bundled reference-data quality caveat with at least one confirmed mislabeled section.

Mitigation: Verify generated readings against the bundled references and disclose uncertainty when a result depends on affected reference data.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/leahlu0124-creator/skills/heluo-lifetime)
- [河洛理数 · 本命卦完整算法](references/heluo-algorithm.md)
- [河洛理数 · 大运与流年算法](references/dayun-liunian.md)
- [河洛理数 · 先天换后天变换法](references/xiantian-houtian.md)
- [河洛理数 raw 文件索引](references/raw-index.md)
- [卷四索引数据](references/juan4_index.json)
- [爻辞知识库](references/yaoci.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown lifetime reading with quoted source passages, plus concise plain-language text for follow-up annual explanations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires birth date/time, approximate birthplace, and gender; outputs should be treated as entertainment and verified against the bundled reference data.]

## Skill Version(s):

1.1.1 (source: server evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
