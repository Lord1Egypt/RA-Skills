## Description: <br>
Morning Wake-Up fetches today's weather, maps conditions to a configured Sonos favorite, and starts playback on the selected speaker. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
People who use Sonos for morning routines use this skill to automate weather-matched music playback, either manually or through a daily OpenClaw cron schedule. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can start Sonos playback automatically and change volume on a local network speaker. <br>
Mitigation: Verify the speaker name, preset favorites, volume, local sonos command, and cron schedule before enabling automation. <br>
Risk: Weather lookup uses a location value, and exact coordinates may reveal precise location. <br>
Mitigation: Use a city-level location instead of exact coordinates when location privacy matters. <br>


## Reference(s): <br>
- [Morning Wake-Up on ClawHub](https://clawhub.ai/terrycarter1985/morning-wake-up) <br>
- [Open-Meteo Geocoding API endpoint](https://geocoding-api.open-meteo.com/v1/search) <br>
- [Open-Meteo Forecast API endpoint](https://api.open-meteo.com/v1/forecast) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and JSON script results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a location and Sonos speaker name, with optional volume and temperature units; volume is clamped to 0-100.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
