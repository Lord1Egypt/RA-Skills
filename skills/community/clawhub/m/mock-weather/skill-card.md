## Description: <br>
Generates simulated current weather and 1-7 day forecasts for any Chinese or English city name when real weather data is unavailable or a mock weather response is acceptable. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[KrisLiu16](https://clawhub.ai/user/KrisLiu16) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to answer weather-style requests with deterministic simulated data for demos, tests, and situations where no real weather API is available. Users should be told that the result is mock data, not an actual weather forecast. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may mistake simulated weather output for a real forecast. <br>
Mitigation: Clearly state that outputs are mock data and avoid using them for weather-sensitive decisions. <br>
Risk: The skill may run the included local Python script when responding to weather-style requests. <br>
Mitigation: Review the script before deployment and install only where local script execution is acceptable. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text weather report with dates, city, condition, temperature range, humidity, and wind fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are generated locally and deterministically from city name and current date; forecasts are limited to 1-7 days.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
