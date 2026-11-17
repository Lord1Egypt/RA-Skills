## Description:

Search and retrieve Magic: The Gathering card data through the Scryfall API, including lookup by name, type, color, mana cost, rules text, set, price, rulings, legality, image, and random-card criteria.

This skill is ready for commercial/non-commercial use.

## Publisher:

[santidev95](https://clawhub.ai/user/santidev95)

### License/Terms of Use:


## Use Case:

External users and MTG-focused agent workflows use this skill to find Magic card information and form Scryfall queries for card lookup, pricing, legality, rulings, images, and random card retrieval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Card search prompts and query terms may be sent to the public Scryfall API.

Mitigation: Avoid submitting private decklists, unreleased strategy notes, or other sensitive information in card search queries.

Risk: Broad MTG trigger wording may activate the skill for general Magic-related prompts.

Mitigation: Confirm that Scryfall lookup is appropriate before making API calls for broad deck-building or rules discussions.

## Reference(s):

- [Scryfall API](https://api.scryfall.com)
- [Scryfall Search Syntax Reference](references/search_syntax.md)
- [ClawHub Skill Page](https://clawhub.ai/santidev95/skills/mtg-edh-deckbuilder)
- [Publisher Profile](https://clawhub.ai/user/santidev95)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown or plain text with optional JSON-derived card details and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call the public Scryfall API and return card names, rules text, legality, prices, image URLs, and related lookup results.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
