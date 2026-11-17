## Description:

MTG (Magic: The Gathering) comprehensive knowledge base assistant that answers rules questions, queries cards in Chinese and English, analyzes card interactions, explains formats and strategies, and tells lore.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raymondeeeemmmm](https://clawhub.ai/user/raymondeeeemmmm)

### License/Terms of Use:

MIT-0

## Use Case:

External Magic: The Gathering players, judges, and agents use this skill to answer rules questions, look up cards in Chinese or English, analyze card interactions, explain formats and strategy, translate MTG content, and cite relevant rules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs users to clone a mutable external repository and run an indexing script that was not included in the reviewed package.

Mitigation: Inspect the cloned repository, pin it to a trusted commit, and run the indexing command in a low-privilege environment without sensitive credentials.

Risk: Card, rules, or translation lookups may send query text to third-party APIs.

Mitigation: Avoid submitting confidential decklists, private rules scenarios, or sensitive user content to external lookup services.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/raymondeeeemmmm/skills/mtg-wiki-en)
- [Full MTG knowledge base repository referenced by artifact](https://github.com/RaymondYHH/mtg-skill.git)
- [mtgch API](https://mtgch.com/api/v1/)
- [Scryfall API](https://api.scryfall.com/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown text with optional inline shell commands and structured card or rules references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May cite MTG rule numbers, bilingual card names, wiki-style cross-links, and lookup commands when relevant.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
