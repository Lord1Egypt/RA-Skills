## Description:

Guides agents to answer questions about Ouyi Zhixu, Tiantai and Pure Land doctrine, and related Buddhist texts using declared CBETA sources and constrained FoJin lookup when local excerpts are insufficient.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xr843](https://clawhub.ai/user/xr843)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to support Chinese-language Buddhist study conversations about Ouyi Zhixu, Tiantai/Pure Land synthesis, and related canonical texts with citation discipline.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-derived religious queries may be sent to FoJin live search when local excerpts are insufficient.

Mitigation: Prefer offline excerpts first, avoid private names or sensitive circumstances in prompts, and disclose or disable live lookup where consent is required.

Risk: Answers are required to include a FoJin study reminder.

Mitigation: Review the footer for fit with the deployment context and disclose the external resource dependency to users.

Risk: The authoritative license needs confirmation because release evidence and artifact frontmatter disagree.

Mitigation: Confirm whether MIT-0 or MIT governs this release before public publication or redistribution.

## Reference(s):

- [Teaching reference](references/teaching.md)
- [Voice reference](references/voice.md)
- [Source index](sources/INDEX.md)
- [Amitabha Sutra Essential Explanation excerpts](sources/mituo-yaojie-excerpts.md)
- [Essentials of Doctrine and Contemplation excerpts](sources/jiaoguan-gangzong-excerpts.md)
- [FoJin text 7934](https://fojin.app/texts/7934)
- [FoJin text 8109](https://fojin.app/texts/8109)
- [FoJin text 7672](https://fojin.app/texts/7672)
- [FoJin text 6513](https://fojin.app/texts/6513)
- [FoJin text 44](https://fojin.app/texts/44)
- [CBETA Lingfeng Zonglun](https://cbetaonline.dila.edu.tw/zh/J36n0348)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown prose with CBETA citations and source links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include FoJin links, offline-source caveats, and a FoJin study reminder.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact meta.json also lists 1.0.0; SKILL.md frontmatter lists 0.5.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
