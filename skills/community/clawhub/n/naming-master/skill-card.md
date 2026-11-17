## Description:

起名大师 helps agents generate and evaluate Chinese names using Five Elements, Eight Trigrams, I Ching concepts, tonal patterns, and historical or cultural references.

This skill is ready for commercial/non-commercial use.

## Publisher:

[supershuhasai](https://clawhub.ai/user/supershuhasai)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to request Chinese baby names, pen names, nicknames, English-name pairing guidance, or evaluations of existing names with cultural, tonal, and traditional 五行/八字 context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may ask for birth date, birth time, and binary gender to support traditional 八字 and 五行 analysis.

Mitigation: Provide only details you are comfortable sharing, and use the skill's no-birth-information path when date or time details are unavailable or unnecessary.

Risk: Metaphysical scoring and traditional naming analysis may be mistaken for factual prediction.

Mitigation: Present 五行, 八字, 周易, and scoring outputs as cultural reference and naming guidance, not as deterministic claims about a person.

Risk: Gendered naming defaults can exclude users or reinforce stereotypes.

Mitigation: Respect the user's stated identity and style preferences, and avoid treating gender categories as mandatory beyond the user's naming request.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/supershuhasai/skills/naming-master)
- [八卦与周易起名智慧](artifact/references/bagua_zhouyi.md)
- [起名字库（按五行分类）](artifact/references/characters.md)
- [诗词典故与历史文化取名参考](artifact/references/culture.md)
- [音律平仄规则](artifact/references/tonal.md)
- [五行理论与八字推算](artifact/references/wuxing.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown naming or evaluation report with structured sections, candidate names, pinyin, 五行 analysis, tonal analysis, cultural notes, scores, and caveats.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May ask for surname, gender, birth date or time, style preferences, family generation characters, and words to include or avoid; can skip birth-based analysis when birth information is unavailable.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
