## Description: <br>
查品牌、车系、车型详情、搜索与热门/销量榜等。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jisuapi](https://clawhub.ai/user/jisuapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to answer vehicle catalog questions such as brand lineups, series details, model searches, popular vehicles, and sales rankings through JisuAPI car data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Vehicle lookup terms, IDs, price filters, ranking parameters, and the API key are sent to JisuAPI and may consume provider quota. <br>
Mitigation: Use a JisuAPI account key intended for this integration, avoid sensitive personal information in search keywords, and monitor provider quota usage. <br>


## Reference(s): <br>
- [JisuAPI Car Models API documentation](https://www.jisuapi.com/api/car) <br>
- [JisuAPI provider homepage](https://www.jisuapi.com/) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON responses and markdown guidance with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and the JISU_API_KEY environment variable; search terms, IDs, price filters, ranking parameters, and the API key are sent to JisuAPI.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
