## Description: <br>
Fetches up to 72 hours of historical weather data from the Caiyun Weather API, including temperature, conditions, precipitation, wind, humidity, apparent temperature, and air quality. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shuowang-ai](https://clawhub.ai/user/shuowang-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to answer recent historical weather questions for specified coordinates and to summarize past conditions over a 1-72 hour lookback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queries send the requested coordinates and Caiyun API token to Caiyun. <br>
Mitigation: Use a dedicated Caiyun token, protect local token storage, and avoid querying exact private locations unless that disclosure is acceptable. <br>


## Reference(s): <br>
- [Caiyun Weather API endpoint](https://api.caiyunapp.com/v2.6) <br>
- [ClawHub skill page](https://clawhub.ai/shuowang-ai/knowair-historical) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [JSON from the helper script with agent-authored text or Markdown summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, internet access, a Caiyun API token, longitude and latitude, and optional hours and language arguments.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
