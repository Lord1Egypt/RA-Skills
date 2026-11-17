## Description:

Search GuruWalk free tours through the GuruWalk MCP server and return bookable options by city, dates, and language.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gdanielwalk](https://clawhub.ai/user/gdanielwalk)

### License/Terms of Use:


## Use Case:

External users and travel-planning agents use this skill to search GuruWalk walking tours for a city, date range, and language, then present concise bookable options with availability and booking links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tour search parameters such as city, date range, and language are sent to an external GuruWalk MCP service.

Mitigation: Confirm vague requests before searching and avoid sending unnecessary personal details.

## Reference(s):

- [GuruWalk MCP server](https://guruwalk-api-44909317956.europe-southwest1.run.app/mcp)
- [ClawHub skill page](https://clawhub.ai/gdanielwalk/skills/guruwalk-free-tours)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Concise Markdown recommendations with tour details, availability, meeting points, and booking URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns ranked options from parsed GuruWalk MCP search results; asks for dates before searching when dates are missing.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
