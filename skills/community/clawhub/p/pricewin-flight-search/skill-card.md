## Description:

Search live flight fares for a route and date across Agoda, Trip.com, and Traveloka for one-way or round-trip travel, with airline, timing, stops, duration, price, and direct booking links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cotghw](https://clawhub.ai/user/cotghw)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel-planning agents use this skill to compare live one-way or round-trip flight fares across Agoda, Trip.com, and Traveloka using IATA route codes, dates, passenger count, and cabin class.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer persistently registers a hosted remote MCP server across detected local agent apps.

Mitigation: Run the dry run first, review the target config files, install only if the hosted PriceWin endpoint is trusted, and keep the .bak backups for removal or rollback.

Risk: Custom --url or PRICEWIN_MCP_URL values can create a Codex TOML injection risk.

Mitigation: Avoid custom MCP URLs unless you control the endpoint and have reviewed the exact value before registration.

Risk: Flight searches send route, date, passenger-count, cabin, and session data to PriceWin's hosted service.

Mitigation: Do not send personal data in query text, review the privacy policy, and treat fares as comparison-only until confirmed by the provider.

## Reference(s):

- [Flight Search Tool Reference](artifact/reference.md)
- [Security and Data Handling](artifact/SECURITY.md)
- [ClawHub Skill Page](https://clawhub.ai/cotghw/skills/pricewin-flight-search)
- [PriceWin Skills Hub](https://github.com/Price-Win/pricewin-skills-hub)
- [PriceWin Privacy Policy](https://price.win/en/privacy-policy)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown flight summaries with provider links and setup commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns top 5-7 flights per leg; fares are comparison-only and time-sensitive.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
