## Description:

Scotty - AT Public Transport Service (ÖBB) helps agents plan Austrian rail journeys, check station arrivals and departures, and retrieve service disruptions for ÖBB, S-Bahn, regional trains, and supported cross-border connections.

This skill is ready for commercial/non-commercial use.

## Publisher:

[manmal](https://clawhub.ai/user/manmal)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to answer Austrian public transport planning questions with shell helpers for station search, journey planning, station arrivals/departures, and service disruptions.

### Deployment Geography for Use:

Austria and supported neighboring-country connections

## Known Risks and Mitigations:

Risk: Travel searches are sent to ÖBB, so station names, dates, times, and route queries may be shared with the external timetable service.

Mitigation: Treat trip-planning inputs as data disclosed to ÖBB and avoid submitting sensitive travel patterns unless that disclosure is acceptable.

Risk: The shell helpers construct JSON request bodies from user-provided station, date, time, and count strings.

Mitigation: Avoid untrusted or unusual inputs until the scripts build JSON with jq and validate numeric, date, and time parameters.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/manmal/skills/oebb-scotty)
- [ÖBB Scotty HAFAS endpoint](https://fahrplan.oebb.at/bin/mgate.exe)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance with bash examples and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and jq; timetable, station, and disruption queries are sent to the ÖBB Scotty HAFAS endpoint.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
