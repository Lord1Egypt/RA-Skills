## Description:

Audit and rewrite Chinese or English content to remove AI tone, protect factual spans, and pull the result toward a target human voice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fendouai](https://clawhub.ai/user/fendouai)

### License/Terms of Use:

MIT-0

## Use Case:

Writers, editors, and developers use this skill to audit, rewrite, or minimally edit Chinese and English prose that sounds formulaic or AI-generated. It is intended for editorial improvement, not for proving whether text was written by a human or an AI system.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Edit mode may modify prose in place, which can change meaning if accepted without review.

Mitigation: Review file diffs before accepting edits; the skill instructs agents to protect numbers, dates, commands, paths, quotes, owners, errors, statuses, and metrics before rewriting.

Risk: AI-tone findings can be mistaken for proof of authorship.

Mitigation: Use findings as editorial quality signals only; the artifact states that these patterns are signals, not proof.

## Reference(s):

- [Server-resolved GitHub repository](https://github.com/fendouai/huorengan)
- [ClawHub skill page](https://clawhub.ai/fendouai/skills/huorengan)
- [Skill definition](https://github.com/fendouai/huorengan/blob/ef4feda4383df734a7864fa198bbd791b28f76ea/SKILL.md)
- [Detector category map](https://github.com/fendouai/huorengan/blob/ef4feda4383df734a7864fa198bbd791b28f76ea/detector/CATEGORIES.md)
- [English phrase references](https://github.com/fendouai/huorengan/blob/ef4feda4383df734a7864fa198bbd791b28f76ea/references/phrases-en.md)
- [Chinese phrase references](https://github.com/fendouai/huorengan/blob/ef4feda4383df734a7864fa198bbd791b28f76ea/references/phrases-zh.md)
- [Protected spans guidance](https://github.com/fendouai/huorengan/blob/ef4feda4383df734a7864fa198bbd791b28f76ea/references/protected-spans.md)
- [Voice contract](https://github.com/fendouai/huorengan/blob/ef4feda4383df734a7864fa198bbd791b28f76ea/references/voice-contract.md)
- [Translation tone guidance](https://github.com/fendouai/huorengan/blob/ef4feda4383df734a7864fa198bbd791b28f76ea/references/translation-tone.md)
- [Structure anti-pattern guidance](https://github.com/fendouai/huorengan/blob/ef4feda4383df734a7864fa198bbd791b28f76ea/references/structures.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Markdown responses with audit findings, rewritten prose, edit summaries, and voice drift notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May edit prose in place when used in edit mode; no external tools or APIs are required.]

## Skill Version(s):

0.1.0 (source: skill frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
