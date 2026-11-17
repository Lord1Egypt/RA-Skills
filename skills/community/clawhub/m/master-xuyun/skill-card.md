## Description:

Provides a Chinese-language Xuyun and Chan teaching assistant that answers questions about Chan practice, meditation methods, monastic discipline, and declared CBETA source texts in Xuyun's voice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xr843](https://clawhub.ai/user/xr843)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to answer Chinese-language questions about Xuyun, Chan meditation, huatou practice, monastic discipline, and related cited Buddhist texts. It is intended for study-oriented guidance and includes reminders to consult qualified teachers for formal practice guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live FoJin lookup may send user query terms to fojin.app when local excerpts are insufficient.

Mitigation: Avoid including personal or sensitive details in source-search questions unless the user is comfortable with those terms being sent to FoJin.

Risk: The skill answers in a fixed Xuyun/Chan teaching style and may not fit users seeking neutral academic or formal practice instruction.

Mitigation: Present responses as study-oriented guidance, keep citations visible, and direct users to qualified teachers or source texts for formal practice decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xr843/skills/master-xuyun)
- [Publisher profile](https://clawhub.ai/user/xr843)
- [Teaching reference](artifact/references/teaching.md)
- [Voice reference](artifact/references/voice.md)
- [Offline source index](artifact/sources/INDEX.md)
- [FoJin: Surangama Sutra, T19n0945](https://fojin.app/texts/65)
- [FoJin: Diamond Sutra, T08n0235](https://fojin.app/texts/7)
- [FoJin: Platform Sutra, T48n2008](https://fojin.app/texts/58)
- [FoJin: Perfect Enlightenment Sutra, T17n0842](https://fojin.app/texts/64)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Chinese-language Markdown answers with inline CBETA citations and FoJin links.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses offline excerpts first and may query FoJin only when declared sources are insufficient; doctrinal claims require citations.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact/meta.json; artifact/SKILL.md frontmatter says 0.5.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
