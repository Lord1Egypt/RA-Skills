## Description:

Magyar nyelvű szövegek elemzését, összefoglalását, kulcsszó- és entitáskinyerését, valamint érzelem- és témaazonosítását segíti.

This skill is ready for commercial/non-commercial use.

## Publisher:

[izsook](https://clawhub.ai/user/izsook)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and Hungarian-language content teams use this skill to guide summarization, keyword extraction, topic identification, sentiment analysis, and entity extraction for Hungarian text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact references stopword, regex, NER, and script files that are not included.

Mitigation: Treat those references as unavailable unless supplied separately; rely only on the bundled Markdown guidance and verify any generated processing logic before use.

Risk: Hungarian NLP outputs such as summaries, sentiment labels, and entity lists can be incomplete or context-sensitive.

Mitigation: Review outputs against the source text, especially where idioms, negation, ambiguous words, dates, or named entities affect decisions.

## Reference(s):

- [Magyar Szövegértés - Best Practices](references/szovegertes.md)
- [ClawHub skill page](https://clawhub.ai/izsook/skills/magyar-szovegfeldolgoz-s)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code]

**Output Format:** [Markdown guidance with illustrative Python snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable files are included in the release artifact.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
