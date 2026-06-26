## Description: <br>
Virtual card deck — shuffle, draw, and manage playing cards via the Deck of Cards API <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucegutman](https://clawhub.ai/user/brucegutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to create shuffled virtual decks, draw cards, and reshuffle decks for card games, decision tools, probability teaching, and shared party games. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends requests to a Pipeworx remote gateway. <br>
Mitigation: Use it only when remote gateway use is acceptable for the deck activity, and avoid sending sensitive local data because the skill does not require it. <br>
Risk: The MCP configuration fetches mcp-remote from npm through npx. <br>
Mitigation: Prefer the direct curl workflow when a narrower execution path is needed, or pin and review the MCP client dependency before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/brucegutman/pipeworx-deckofcards) <br>
- [Pipeworx Deck of Cards pack](https://pipeworx.io/packs/deckofcards) <br>
- [Pipeworx Deck of Cards MCP gateway](https://gateway.pipeworx.io/deckofcards/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text] <br>
**Output Format:** [Markdown with inline bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces instructions and remote tool calls for deck creation, card drawing, and deck shuffling.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
