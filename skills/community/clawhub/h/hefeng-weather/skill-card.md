## Description: <br>
Queries real-time weather, hourly forecasts, daily forecasts, and minute-level precipitation for a specified city using the QWeather/HeFeng Weather API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aaronjager92](https://clawhub.ai/user/aaronjager92) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to answer city weather questions in chat workflows or from the command line after configuring a QWeather API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a QWeather/HeFeng API key and supports reading it from a local config file. <br>
Mitigation: Prefer the HEFENG_WEATHER_API_KEY environment variable, do not commit config.txt, and rotate exposed keys. <br>
Risk: The setup documentation contains conflicting API-key acquisition links. <br>
Mitigation: Use the official QWeather key page at https://id.qweather.com/ when provisioning credentials. <br>
Risk: Broad chat triggers for routine weather comments may consume paid API quota unexpectedly. <br>
Mitigation: Narrow trigger phrases, monitor QWeather usage, and apply quota controls where available. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/aaronjager92/hefeng-weather) <br>
- [QWeather API key registration](https://id.qweather.com/) <br>
- [Artifact reference README](artifact/references/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text weather summaries and Markdown setup guidance with shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a QWeather/HeFeng API key; accepts a city name or city ID plus a forecast type.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
