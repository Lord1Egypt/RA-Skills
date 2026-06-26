## Description: <br>
Fetch upcoming events from Luma (lu.ma) for any city, returning event details including venue, date, hosts, ticket status, and links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[firefrog-pepe](https://clawhub.ai/user/firefrog-pepe) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to find public Luma events for cities, compare event options, and return event details such as venue, time, hosts, ticket status, and links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts lu.ma public event pages when fetching city event listings. <br>
Mitigation: Install only when outbound requests to Luma are acceptable for the agent environment. <br>
Risk: Recently fetched event results are retained in a local OpenClaw workspace cache. <br>
Mitigation: Delete the luma-events.json cache when retained event data is no longer wanted. <br>
Risk: Luma page structure changes or unsupported city pages may return empty or failed results. <br>
Mitigation: Treat empty results as page-format dependent and retry or verify directly on Luma when event completeness matters. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/firefrog-pepe/luma-enhanced) <br>
- [Luma city pages](https://lu.ma/{city_slug}) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, files] <br>
**Output Format:** [Human-readable text or JSON event arrays, with fetched results persisted to a local JSON cache.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3; accepts one or more city slugs plus optional day range, result limit, and JSON output flags.] <br>

## Skill Version(s): <br>
1.1.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
