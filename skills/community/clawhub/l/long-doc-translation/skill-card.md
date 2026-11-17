## Description:

Guides full-text translation of authorized long-form German, English, French, and Japanese works into a Chinese manuscript, a self-contained HTML reader, segment-level review files, and a terminology glossary, flagging uncertain passages for human review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huhoo](https://clawhub.ai/user/huhoo)

### License/Terms of Use:

MIT-0

## Use Case:

Translators and researchers use this workflow to manage large-book translation, maintain consistent terminology and formatting across segments, and review uncertain passages and merge quality before delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An optional OCR service may receive sensitive source documents.

Mitigation: Review the OCR provider's privacy practices before submitting sensitive material; skip OCR when text is already available.

Risk: Translation and chunk-merging issues can leave errors, duplicate passages, gaps, or uncertain wording in the final manuscript.

Mitigation: Keep a manuscript backup, inspect QA reports rather than relying on exit codes, manually check suspected duplicates, and send uncertain passages for human review.

Risk: Publishing source text without authorization or using a draft as practice-grade legal output is outside the skill's stated scope.

Mitigation: Use only source material you are authorized to access, do not publish copyrighted text as-is, and obtain qualified review for legal work.

## Reference(s):

- [ClawHub Skill Release](https://clawhub.ai/huhoo/skills/long-doc-translation)
- [Publisher Profile](https://clawhub.ai/user/huhoo)
- [Parallel Translation Guide](references/parallel-translation.md)
- [Translation Pitfalls](references/pitfalls.md)
- [QA Checklist](references/qa-checklist.md)
- [Reader Build Guide](references/reader-build.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, HTML, Files]

**Output Format:** [Chinese translation manuscript in Markdown, a self-contained HTML reader, segment-level review files, and a terminology glossary.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uncertain passages are flagged for human review; source coverage and translation quality require review before delivery.]

## Skill Version(s):

1.3.18 (source: SKILL.md frontmatter, CHANGELOG, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
