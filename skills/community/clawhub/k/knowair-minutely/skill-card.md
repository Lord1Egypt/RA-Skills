## Description: <br>
Get minute-level precipitation forecast for the next 2 hours via the Caiyun Weather API, including 1-minute precipitation intensity and 30-minute probability data for locations with supported coverage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shuowang-ai](https://clawhub.ai/user/shuowang-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to answer near-term rain questions, such as whether to bring an umbrella or when precipitation may start or stop, by querying minute-level Caiyun Weather API data for longitude and latitude coordinates. <br>

### Deployment Geography for Use: <br>
Global; forecast data is mainly available for China and works best for major Chinese cities. <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Caiyun Weather API token and sends requested longitude and latitude coordinates to Caiyun. <br>
Mitigation: Use a token scoped to this service, protect it through CAIYUN_TOKEN or the documented local token file, and only query coordinates you are comfortable sending to Caiyun. <br>
Risk: Minute-level precipitation data may be unavailable or limited for unsupported locations. <br>
Mitigation: When the API has no minutely data, tell the user that coverage is mainly available for China and avoid overstating forecast precision. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shuowang-ai/knowair-minutely) <br>
- [Publisher profile](https://clawhub.ai/user/shuowang-ai) <br>
- [Caiyun Weather API endpoint](https://api.caiyunapp.com/v2.6) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON from the helper script plus concise natural-language precipitation guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, internet access, CAIYUN_TOKEN, and longitude/latitude coordinates; supports English or Chinese output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
