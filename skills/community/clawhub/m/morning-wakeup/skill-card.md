## Description: <br>
Morning wake-up automation that fetches today's weather and matches a Sonos playback preset. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and home-automation developers use this skill to run a daily weather-aware Sonos wake-up routine, either on demand or from a scheduled cron flow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can control a user-named Sonos speaker and set its volume. <br>
Mitigation: Install only when speaker control is intended, confirm the speaker name before scheduling, and keep the configured volume within an acceptable range. <br>
Risk: The configured city or coordinates are sent to Open-Meteo for geocoding and weather lookup. <br>
Mitigation: Use a city-level location when precise coordinates are unnecessary and inform users that weather lookup depends on Open-Meteo. <br>
Risk: The script invokes the local sonos CLI. <br>
Mitigation: Use a trusted Sonos CLI installation and review presets before enabling unattended cron runs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/terrycarter1985/morning-wakeup) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown instructions with bash and JSON examples; runtime script emits a JSON status object.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a trusted local Sonos CLI, a reachable Sonos speaker, and Open-Meteo network access for weather lookup.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
