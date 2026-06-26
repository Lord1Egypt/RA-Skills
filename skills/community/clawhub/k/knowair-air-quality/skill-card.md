## Description: <br>
Gets hourly and daily weather forecasts by latitude and longitude via the Caiyun Weather API, including temperature, conditions, precipitation probability, wind, humidity, life indices, and daily AQI when available. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shuowang-ai](https://clawhub.ai/user/shuowang-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to retrieve forecast data for specific coordinates and present concise daily or hourly weather summaries. It is useful for answering questions about upcoming conditions, rain windows, temperature trends, wind, humidity, life indices, and available daily AQI values. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends the configured Caiyun API token and queried coordinates to Caiyun when fetching forecasts. <br>
Mitigation: Use a token intended for this service and avoid querying locations considered sensitive. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shuowang-ai/knowair-air-quality) <br>
- [Caiyun Weather API endpoint](https://api.caiyunapp.com/v2.6) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON forecast results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, internet access, CAIYUN_TOKEN, and longitude/latitude coordinates; supports English and Chinese output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
