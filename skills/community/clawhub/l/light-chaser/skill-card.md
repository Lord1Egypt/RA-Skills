## Description: <br>
Light Chaser helps travelers turn destination, date, equipment, weather, and location research into an executable travel photography shooting timeline. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ccshen722](https://clawhub.ai/user/ccshen722) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel photographers use this skill to plan where, when, and how to shoot during a trip. It gathers destination, travel date, and equipment details, then combines scenic spot research, weather context, timing guidance, shooting techniques, and editing suggestions into a practical plan. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may send destination and travel-date context to web search or QWeather API endpoints for weather and location planning. <br>
Mitigation: Use it only when this lookup behavior is acceptable for the itinerary, and avoid entering sensitive private travel details. <br>
Risk: A configured QWeather API key in config.env could be exposed if unrelated secrets are stored in the same file or if the skill directory is shared. <br>
Mitigation: Use a dedicated QWeather key and keep unrelated secrets out of config.env. <br>
Risk: Fallback weather gathered through web search may be less precise than API weather data. <br>
Mitigation: Treat generated timing and weather-dependent recommendations as planning guidance and verify critical conditions before travel. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ccshen722/light-chaser) <br>
- [QWeather Developer Platform](https://dev.qweather.com/) <br>
- [DJI Fly Safe](https://www.dji.com/cn/flysafe) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Guidance] <br>
**Output Format:** [Markdown travel photography timeline with weather summary, route-aware shooting schedule, capture guidance, wardrobe suggestions, and editing direction.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use web search or optional QWeather API configuration; weather precision depends on the configured data source.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
