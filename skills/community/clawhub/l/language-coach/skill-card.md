## Description:

Language Coach provides multi-language writing corrections for grammar, word choice, collocations, and idiom errors in English, Chinese, Spanish, French, and Japanese.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaigegao1110](https://clawhub.ai/user/kaigegao1110)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and developers use this skill to get brief, educational corrections for user-provided English, Chinese, Spanish, French, and Japanese text. It is intended for grammar, word choice, collocation, idiom, register, and language-specific usage issues, activated by explicit language commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing from an unreviewed GitHub source may use content different from the server-reviewed ClawHub release.

Mitigation: Install from the ClawHub/OpenClaw package path when possible, or use a reviewed tag or commit and verify the source first.

Risk: Correction behavior could be invoked when the user does not intend language review.

Mitigation: Use explicit //en, //cn, //es, //fr, or //ja commands when correction behavior is desired.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kaigegao1110/skills/language-coach)
- [Language Coach Homepage](https://github.com/KaigeGao1110/language-coach)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown text with original text, corrected text, and a brief explanation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces at most one meaningful correction per message and returns no output when no correction is needed beyond confirming the original text is acceptable.]

## Skill Version(s):

2.0.3 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
