## Description:

Virtual card deck - shuffle, draw, and manage playing cards via the Deck of Cards API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucegutman](https://clawhub.ai/user/brucegutman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to create, shuffle, draw from, and reshuffle virtual playing-card decks for games, probability exercises, decision tools, and shared activities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup uses a mutable npm package version for the MCP bridge, which can introduce local supply-chain risk.

Mitigation: Use a pinned, reviewed version of mcp-remote before installation.

Risk: The MCP process may receive more local access than it needs.

Mitigation: Run it with minimal environment access and avoid exposing secrets or broad filesystem permissions.

## Reference(s):

- [Pipeworx Deck of Cards homepage](https://pipeworx.io/packs/deckofcards)
- [ClawHub skill page](https://clawhub.ai/brucegutman/skills/pipeworx-deckofcards)
- [Deck of Cards MCP endpoint](https://gateway.pipeworx.io/deckofcards/mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls]

**Output Format:** [Markdown with JSON configuration and inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tool calls return deck identifiers, card codes, suits, values, and card image URLs.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
