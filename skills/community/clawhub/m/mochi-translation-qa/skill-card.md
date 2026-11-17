## Description:

Translate or polish user-provided text with the current model, then check bilingual segment alignment, required terminology, numbers and links and export a comparison with review issues. Use for Translation and Proofreading, translation reviews or bilingual delivery; mechanical checks do not certify meaning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hznetnewpower](https://clawhub.ai/user/hznetnewpower)

### License/Terms of Use:

MIT-0

## Use Case:

Translators, editors, and teams use this skill to translate or polish user-provided text or review bilingual drafts, then check segment alignment, required terminology, numbers, and links and export reports for human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The connected model processes supplied text, and local reports retain the source and translation.

Mitigation: Avoid unnecessary sensitive data and use appropriate privacy settings.

Risk: Mechanical checks do not establish whether a translation preserves meaning, tone, negation, or units.

Mitigation: Review the translation manually for meaning and context before relying on it.

## Reference(s):

- [Translation input and outputs](references/input.md)
- [ClawHub release page](https://clawhub.ai/hznetnewpower/skills/mochi-translation-qa)
- [GitHub folder referenced in README](https://github.com/hznetnewpower/mochilab-free-skills/tree/main/skills/mochi-translation-qa)

## Skill Output:

**Output Type(s):** [Text, Markdown, CSV, JSON, Guidance]

**Output Format:** [Translated or polished text and bilingual Markdown/CSV comparisons with a JSON issue report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports align source and target segments and flag terminology, number, and link issues; meaning requires human review.]

## Skill Version(s):

1.0.1 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
