## Description: <br>
Query Odds-API.io for sports events, bookmakers, and betting odds, including event search and odds retrieval by event ID; requires a user-provided API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diegopetrucci](https://clawhub.ai/user/diegopetrucci) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, developers, and agents use this skill to search sports events, list sports and bookmakers, and retrieve betting odds through the Odds-API.io v3 API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A real Odds-API.io API key can be exposed if dry-run output is shared or logged. <br>
Mitigation: Use ODDS_API_KEY instead of pasting keys into chat and avoid dry-run with a real key unless the output remains private. <br>
Risk: Changing the API destination can send requests and API keys to an untrusted endpoint. <br>
Mitigation: Use --base-url only with a trusted Odds-API.io-compatible endpoint. <br>


## Reference(s): <br>
- [Odds-API.io quick reference](references/odds-api-reference.md) <br>
- [Odds-API.io v3 API base URL](https://api.odds-api.io/v3) <br>
- [ClawHub skill page](https://clawhub.ai/diegopetrucci/odds-checker-api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON API response guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include compact summaries or JSON returned by Odds-API.io when the helper script is executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
