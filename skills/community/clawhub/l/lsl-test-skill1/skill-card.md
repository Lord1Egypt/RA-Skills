## Description: <br>
查询城市当前天气，并用简洁中文返回天气状况和温度。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lushulin-jack](https://clawhub.ai/user/lushulin-jack) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to look up current weather for a city and return a short Chinese-language answer with the city name, weather condition, and temperature. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Weather lookup depends on an external public endpoint and city-name interpretation, so results can fail or be inaccurate. <br>
Mitigation: Review weather responses before relying on them and ask users to retry with an English city name when lookup fails. <br>
Risk: The skill performs a network request for the requested city. <br>
Mitigation: Grant network access only for the intended weather lookup and avoid sending sensitive data as part of the city query. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lushulin-jack/lsl-test-skill1) <br>


## Skill Output: <br>
**Output Type(s):** [Text] <br>
**Output Format:** [Plain text in Chinese] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Expected response is 1-2 sentences and includes city name, weather condition, and temperature.] <br>

## Skill Version(s): <br>
1.0.4 (source: ClawHub server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
