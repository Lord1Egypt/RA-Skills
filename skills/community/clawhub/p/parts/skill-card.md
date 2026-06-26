## Description: <br>
查配件品牌、OE 号模糊搜、适用车型与替换件等。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jisuapi](https://clawhub.ai/user/jisuapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query JisuAPI auto-parts OE data for part brands, fuzzy OE part-number matches, compatible sale vehicles, and replacement parts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Part numbers, brand IDs, parts IDs, and the configured JisuAPI key are sent to JisuAPI during lookups. <br>
Mitigation: Use the skill only when sharing those lookup values with JisuAPI is acceptable, and prefer a dedicated API key with limited quota. <br>
Risk: The Python requests dependency is required to call the API. <br>
Mitigation: Install requests from a trusted package source and keep the runtime environment controlled. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/jisuapi/parts) <br>
- [JisuAPI website](https://www.jisuapi.com/) <br>
- [JisuAPI Auto Parts OE API documentation](https://www.jisuapi.com/api/parts/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, the requests dependency, and JISU_API_KEY.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
