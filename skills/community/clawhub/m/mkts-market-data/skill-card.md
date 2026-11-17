## Description:

Retrieve market data and support research for stocks, crypto, ETFs, commodities, and forex, with explicitly confirmed portfolio, journal, and watchlist workflows through mkts.io.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdliriano](https://clawhub.ai/user/sdliriano)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use the skill for market research, quotes, screening, financial news, and user-requested portfolio, journal, or watchlist management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Portfolio positions, journal text, and watchlists can reveal sensitive financial interests when sent to mkts.io and stored in the API-key owner's account.

Mitigation: Keep requests read-only by default, minimize private content, and show the exact payload and obtain informed confirmation before each account change or sensitive submission.

Risk: Account deletions have no documented undo and may affect the wrong records if the target is not resolved first.

Mitigation: Fetch records first, identify the exact ID or affected count, explain the lack of a documented undo, and obtain confirmation immediately before deletion.

## Reference(s):

- [mkts.io API](https://mkts.io/api/v1)
- [mkts Examples](https://github.com/mkts-io/mkts-examples)
- [ClawHub release](https://clawhub.ai/sdliriano/skills/mkts-market-data)

## Skill Output:

**Output Type(s):** [JSON, Text, Guidance]

**Output Format:** [Structured market data and natural-language summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Account workflows may involve private financial records.]

## Skill Version(s):

1.0.19 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
