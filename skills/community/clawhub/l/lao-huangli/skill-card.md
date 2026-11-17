## Description:

Use when users ask for Lao Huangli, Huangli, date selection, auspicious and inauspicious activities, clashes, sexagenary calendar fields, solar terms, or need a reproducible workflow to compute traditional Chinese almanac recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cikichen](https://clawhub.ai/user/cikichen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and users consulting traditional Chinese almanac data use this skill to calculate lunar calendar fields, sexagenary cycle values, solar terms, daily recommendations, and explain which results are deterministic versus ruleset-derived.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency installation and astronomy data caching may download Python packages or a JPL ephemeris file.

Mitigation: Use trusted package sources, pin hashes or a lockfile, and pre-provision and verify de440s.bsp in stricter environments.

Risk: Almanac recommendations may be mistaken for legal, medical, financial, safety, or other high-stakes advice.

Mitigation: Treat outputs as cultural reference only and include disclaimers when presenting recommendations.

Risk: Different almanac profiles, year boundaries, day boundaries, and ruleset variants can produce different results.

Mitigation: State the selected profile, timezone, year boundary, day boundary, ruleset version, and source references in user-facing output.

## Reference(s):

- [Lao Huangli ClawHub Skill](https://clawhub.ai/cikichen/skills/lao-huangli)
- [Calculation Pipeline](artifact/references/calculation-pipeline.md)
- [Rules and Variants](artifact/references/rules-and-variants.md)
- [Qinding Xieji Bianfangshu, Volume 1](https://zh.wikisource.org/zh-hans/%E6%AC%BD%E5%AE%9A%E5%8D%94%E7%B4%80%E8%BE%A8%E6%96%B9%E6%9B%B8_(%E5%9B%9B%E5%BA%AB%E5%85%A8%E6%9B%B8%E6%9C%AC)/%E5%8D%B701)
- [Qinding Xieji Bianfangshu, Volume 4](https://zh.wikisource.org/zh-hans/%E6%AC%BD%E5%AE%9A%E5%8D%94%E7%B4%80%E8%BE%A8%E6%96%B9%E6%9B%B8_(%E5%9B%9B%E5%BA%AB%E5%85%A8%E6%9B%B8%E6%9C%AC)/%E5%8D%B704)
- [Qinding Xieji Bianfangshu, Volume 7](https://zh.wikisource.org/wiki/%E6%AC%BD%E5%AE%9A%E5%8D%94%E7%B4%80%E8%BE%A8%E6%96%B9%E6%9B%B8_(%E5%9B%9B%E5%BA%AB%E5%85%A8%E6%9B%B8%E6%9C%AC)/%E5%8D%B707)
- [Qinding Xieji Bianfangshu, Volume 10](https://zh.wikisource.org/zh-hans/%E6%AC%BD%E5%AE%9A%E5%8D%94%E7%B4%80%E8%BE%A8%E6%96%B9%E6%9B%B8_(%E5%9B%9B%E5%BA%AB%E5%85%A8%E6%9B%B8%E6%9C%AC)/%E5%8D%B710)
- [6tail lunar-javascript](https://github.com/6tail/lunar-javascript)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown, JSON, and plain text calendar output with explanatory prose.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should include the date, timezone, year and day boundary settings, selected ruleset or profile, provenance/source references for rule-derived fields, and cultural-reference disclaimers.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
