## Description:

Translate Chinese pinyin initialisms and internet abbreviations to their possible full Chinese meanings, supporting multiple terms at once.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jayegt002](https://clawhub.ai/user/jayegt002)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to look up Chinese pinyin initialisms, internet slang abbreviations, and ambiguous letter strings, including batch queries with multiple possible interpretations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Lookup text is sent to a third-party API.

Mitigation: Avoid using the skill with secrets, personal data, or confidential text; use explicit short abbreviation lookups.

Risk: Abbreviations may have multiple meanings or pending-review results.

Mitigation: Treat returned meanings as candidates and review the surrounding context before relying on an interpretation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jayegt002/skills/nbnhhsh-skill)
- [nbnhhsh API endpoint](https://lab.magiconch.com/api/nbnhhsh/guess)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell command examples and API result interpretation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return multiple candidate meanings for one abbreviation; queries are sent to a third-party API.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
