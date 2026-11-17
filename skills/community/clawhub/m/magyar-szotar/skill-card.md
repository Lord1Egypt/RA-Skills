## Description:

Provides quick lookup of Hungarian word meanings, synonyms, idioms, expressions, and linguistic analysis from local references or public web sources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[izsook](https://clawhub.ai/user/izsook)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to answer Hungarian dictionary questions, find synonyms, explain idioms and proverbs, and support lightweight Hungarian linguistic analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Public web fallback can send lookup terms or batches to external dictionary services.

Mitigation: Use local reference files for confidential terms, or get user approval before external lookup.

Risk: Dictionary and proverb references may be incomplete, dated, or fail to cover uncommon terms.

Mitigation: Disclose uncertainty, check source freshness, and suggest alternatives when a term is not found.

## Reference(s):

- [Arcanum - Magyar Ertelmezo Szotar](https://www.arcanum.com/hu/online-kiadvanyok/Lexikonok-a-magyar-nyelv-ertelmezo-szotara-1BE8B/)
- [Wiktionary Hungarian](https://hu.wiktionary.org/)
- [Sztaki Szotar](https://dict.sztaki.hu/)
- [references/arcanum-ertsz.md](references/arcanum-ertsz.md)
- [references/kozmondasok.md](references/kozmondasok.md)
- [references/magyar-szotar.json](references/magyar-szotar.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown or plain text responses with dictionary entries, synonym lists, idiom explanations, examples, and lookup guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use local reference data first and public dictionary services as fallback when appropriate.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
