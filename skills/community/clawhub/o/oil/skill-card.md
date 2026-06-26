## Description: <br>
Looks up current gasoline and diesel reference prices for Chinese provinces and cities, and can list supported regions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jisuapi](https://clawhub.ai/user/jisuapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to answer oil-price questions for Chinese provinces or cities, including 92/95/98 gasoline, diesel prices, and supported province lists. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a JisuAPI AppKey and sends province lookup queries to JisuAPI. <br>
Mitigation: Use a dedicated API key where possible, limit its permissions, and monitor quota or billing usage. <br>
Risk: Oil-price answers depend on JisuAPI availability and the freshness of returned data. <br>
Mitigation: Surface the returned update time when available and handle API errors or missing province data explicitly. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jisuapi/oil) <br>
- [JisuAPI Oil API documentation](https://www.jisuapi.com/api/oil/) <br>
- [JisuAPI homepage](https://www.jisuapi.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [JSON API results and concise natural-language answers] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and JISU_API_KEY; sends province lookup requests to JisuAPI.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
