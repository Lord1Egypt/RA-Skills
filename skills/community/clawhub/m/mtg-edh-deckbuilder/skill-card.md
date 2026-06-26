## Description: <br>
Search and retrieve Magic: The Gathering card data using the Scryfall API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[santidev95](https://clawhub.ai/user/santidev95) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to search Magic: The Gathering cards, retrieve card details, inspect legalities and prices, and format Scryfall results for card-information workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Card-search prompts are sent to the external Scryfall API. <br>
Mitigation: Avoid including unrelated private information in card-search prompts. <br>
Risk: Ambiguous Magic or card-like names may trigger an external lookup. <br>
Mitigation: Ask for clarification before lookup when the user's intent is unclear. <br>


## Reference(s): <br>
- [Scryfall API](https://api.scryfall.com) <br>
- [Scryfall Search Syntax Reference](references/search_syntax.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/santidev95/mtg-edh-deckbuilder) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, guidance] <br>
**Output Format:** [Markdown or plain text with optional JSON-formatted Scryfall API responses and shell command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include card names, mana costs, type lines, oracle text, images, prices, set details, legalities, search-result counts, and API error messages.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
