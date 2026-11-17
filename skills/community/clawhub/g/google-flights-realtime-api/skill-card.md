## Description:

Search Google Flights for real-time one-way and round-trip flight deals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mtnrabi](https://clawhub.ai/user/mtnrabi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-focused agents use this skill to search and compare one-way or round-trip flights by route, date, price, stops, airlines, time windows, seat class, and passenger details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may generate and run parallel shell scripts with user-derived flight-search values.

Mitigation: Review generated commands before execution and prefer structured HTTP calls or safely quoted scripts with validated dates, airports, and filters.

Risk: Broad date, destination, or trip-length ranges can fan out into many paid RapidAPI requests.

Mitigation: Set explicit request limits, batch large searches, monitor quota, and ask for confirmation before high-volume searches.

Risk: Invalid or ambiguous airport codes and dates can produce incorrect searches or failed API calls.

Mitigation: Validate IATA codes and date formats before making requests, and ask the user only when required route or date fields cannot be inferred.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mtnrabi/skills/google-flights-realtime-api)
- [Google Flights Live API on RapidAPI](https://rapidapi.com/mtnrabi/api/google-flights-live-api)
- [Google Flights Live API pricing](https://rapidapi.com/mtnrabi/api/google-flights-live-api/pricing)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON request bodies and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Flight results may include airline, price, duration, stops, departure and arrival times, and booking details.]

## Skill Version(s):

1.0.5 (source: server release metadata; artifact frontmatter and artifact/clawhub.json show 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
