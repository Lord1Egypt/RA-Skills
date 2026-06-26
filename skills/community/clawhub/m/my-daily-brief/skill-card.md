## Description: <br>
Generates a concise daily brief with Beijing weather and Baidu trending topics when requested or on a daily schedule. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JokerZeng](https://clawhub.ai/user/JokerZeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users can ask for a quick daily brief covering Beijing weather and Baidu hot-search topics. The skill is not intended for detailed weather forecasts or in-depth news analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The trigger schedule is inconsistent across the evidence, which may cause unexpected automatic daily briefings. <br>
Mitigation: Confirm the intended schedule before enabling automatic runs. <br>
Risk: The skill contacts public weather and Baidu pages when it runs. <br>
Mitigation: Use it only in environments where those external public web requests are acceptable. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/JokerZeng/my-daily-brief) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands] <br>
**Output Format:** [Markdown-like daily brief with weather and ranked trending-topic lines] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fetches public weather data and Baidu trending topics when run; no API credentials are indicated.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
