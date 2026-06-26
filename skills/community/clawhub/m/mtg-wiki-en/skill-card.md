## Description: <br>
MTG Wiki is a Magic: The Gathering knowledge assistant for rules questions, bilingual card lookup, card interaction analysis, formats, strategy, lore, and article translation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[raymondeeeemmmm](https://clawhub.ai/user/raymondeeeemmmm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to answer Magic: The Gathering questions with rule citations, bilingual card data, interaction analysis, format and strategy context, lore, and translated article output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Card lookup terms may be sent to mtgch or Scryfall when API-backed searches are used. <br>
Mitigation: Use the skill only when sharing MTG lookup terms with those services is acceptable, or prefer local database lookups where available. <br>
Risk: The full local database workflow asks users to clone a linked repository and run Python scripts. <br>
Mitigation: Review the repository and scripts before cloning or running them, and run local indexing commands in an isolated environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/raymondeeeemmmm/mtg-wiki-en) <br>
- [mtgch API](https://mtgch.com/api/v1/) <br>
- [Scryfall API](https://api.scryfall.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with rule citations, bilingual card names, reference tables, glossary sections, and inline shell commands when local lookup tools are needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose local Python lookup commands and may rely on mtgch or Scryfall for API-backed card searches.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
