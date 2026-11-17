## Description:

Morning Wake-Up automates a morning routine by fetching current weather, mapping it to a configured Sonos playback preset, and playing it on a named speaker.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

External users and home automation developers use this skill to run a weather-aware morning alarm that selects Sonos music based on current conditions and can be scheduled as a recurring routine.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The configured location or coordinates are shared with Open-Meteo to fetch weather.

Mitigation: Use only locations the user is comfortable sharing and prefer coarse city-level input when precise coordinates are unnecessary.

Risk: The skill controls a named Sonos speaker and can be scheduled as a recurring automation.

Mitigation: Confirm the target speaker, preset, and volume before enabling the routine, and keep a clear way to disable any cron schedule.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/terrycarter1985/skills/morning-wake-up)
- [Open-Meteo geocoding API](https://geocoding-api.open-meteo.com/v1/search)
- [Open-Meteo forecast API](https://api.open-meteo.com/v1/forecast)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with inline shell commands and JSON status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a location, a Sonos speaker name, configured Sonos favorites, and local Sonos CLI access.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
