## Description:

Morning wake-up automation that fetches today's weather and matches a Sonos playback preset.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

External users and automation-minded developers use this skill to set up a weather-aware morning routine that selects a Sonos favorite and plays it on a named speaker, either manually or on a daily schedule.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configured location or coordinates are sent to Open-Meteo for weather lookup.

Mitigation: Use only locations or coordinates you are comfortable sharing with Open-Meteo.

Risk: The skill can control a named Sonos speaker and start playback on a schedule.

Mitigation: Review the speaker name, volume, and cron schedule before enabling recurring runs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/terrycarter1985/skills/morning-wakeup)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with shell commands and a JSON execution result]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a location and Sonos speaker name; optional settings include volume and temperature units.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
