## Description:

Query PokerPal poker game data - games, players, buy-ins, settlements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vvardhan14](https://clawhub.ai/user/vvardhan14)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to query live PokerPal groups, games, player buy-ins, chip counts, and settlement-related results through configured PokerPal bot access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Poker buy-ins, chip counts, player statistics, and settlement results may expose private group financial information.

Mitigation: Install only for authorized users and treat retrieved PokerPal data as private unless the poker group has agreed it may be disclosed.

Risk: The skill sends the bot API key to a configurable PokerPal API endpoint.

Mitigation: Use a least-privileged read-only bot key and set POKERPAL_API_URL only to a trusted HTTPS PokerPal endpoint.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vvardhan14/skills/pokerpal)
- [Publisher profile](https://clawhub.ai/user/vvardhan14)

## Skill Output:

**Output Type(s):** [API Calls, Text, Markdown, Guidance]

**Output Format:** [Markdown or text responses summarizing PokerPal API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses configured POKERPAL_API_URL and POKERPAL_BOT_API_KEY environment variables to retrieve group, game, player, buy-in, and summary data.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
