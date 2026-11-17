## Description:

Query Odds-API.io for sports events, bookmakers, and betting odds; use when an agent needs to call the Odds-API.io v3 API or interpret its responses with a user-provided API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diegopetrucci](https://clawhub.ai/user/diegopetrucci)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to search sports events, identify event IDs, list bookmakers, and retrieve betting odds from Odds-API.io.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dry-run output can expose the user's Odds-API.io API key in a printed request URL.

Mitigation: Use dry-run only with non-production credentials or after removing the key from the command and environment.

Risk: A custom API base URL can direct credential-bearing requests to an untrusted endpoint.

Mitigation: Avoid the custom base URL option except for trusted test endpoints, and use non-production keys when testing.

Risk: The API key can be broadly exposed through the runtime environment.

Mitigation: Prefer a narrowly scoped execution environment for ODDS_API_KEY and avoid storing credentials in skill files or shared logs.

## Reference(s):

- [Odds-API.io quick reference](references/odds-api-reference.md)
- [Odds-API.io v3 API base URL](https://api.odds-api.io/v3)
- [ClawHub skill page](https://clawhub.ai/diegopetrucci/skills/odds-checker-api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, API calls, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON or text API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-provided Odds-API.io API key; the skill instructs users not to store credentials in the skill.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
