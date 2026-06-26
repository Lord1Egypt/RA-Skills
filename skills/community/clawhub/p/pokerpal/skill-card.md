## Description: <br>
Query PokerPal poker game data, including games, players, buy-ins, and settlements. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vvardhan14](https://clawhub.ai/user/vvardhan14) <br>

### License/Terms of Use: <br>


## Use Case: <br>
PokerPal users and agents use this skill to look up live poker group, game, player, buy-in, chip count, and settlement information through configured PokerPal API access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent can access poker group, player, buy-in, chip count, and net result information available to the configured bot key. <br>
Mitigation: Use a read-only, least-privilege PokerPal bot key and rotate it if the endpoint or installation source is no longer trusted. <br>
Risk: The configured PokerPal API URL determines where the bot key is sent. <br>
Mitigation: Install only with a trusted PokerPal API URL and verify the endpoint before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vvardhan14/pokerpal) <br>


## Skill Output: <br>
**Output Type(s):** [text, API calls, guidance] <br>
**Output Format:** [Markdown or plain text responses based on JSON API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires POKERPAL_API_URL and POKERPAL_BOT_API_KEY environment variables.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
