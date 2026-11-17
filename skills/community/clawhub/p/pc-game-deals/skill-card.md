## Description:

Track PC game discounts across Steam, Epic Games, GOG, Humble Store and 30+ stores via CheapShark API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pazzilivo](https://clawhub.ai/user/pazzilivo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to look up PC game discounts, lowest prices, hot deals, price history, and CheapShark web price-alert paths. It is scoped to PC game stores and does not cover console or mobile game deals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Command examples interpolate user-controlled game names and IDs into shell commands.

Mitigation: Use safe argument handling such as curl --get with --data-urlencode for game titles, validate game IDs before use, and avoid executing raw user text as shell syntax.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/pazzilivo/skills/pc-game-deals)
- [CheapShark Stores API](https://www.cheapshark.com/api/1.0/stores)
- [CheapShark Game Search API](https://www.cheapshark.com/api/1.0/games?title=GAME_NAME&limit=5)
- [CheapShark Deals API](https://www.cheapshark.com/api/1.0/deals?storeID=1&upperPrice=15&pageSize=10)
- [CheapShark Game Details API](https://www.cheapshark.com/api/1.0/games?id=GAME_ID)
- [CheapShark Website](https://www.cheapshark.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline bash commands and jq output examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and jq; no API key is required.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
