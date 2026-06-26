## Description: <br>
查询即刻数据菜谱接口，支持食材列表、菜谱搜索、菜谱详情和随机菜谱，并返回菜名、分类、耗时、口味、烹饪方式、主料辅料和做法步骤。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jikeapi-cn](https://clawhub.ai/user/jikeapi-cn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to look up recipe ingredients, search recipes by name, fetch full recipe steps by ID, or request random recipe recommendations through JikeAPI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a JikeAPI AppKey, and full request URLs include the AppKey. <br>
Mitigation: Set the AppKey with the documented environment variable, avoid passing it on the command line, and treat request URLs as sensitive. <br>
Risk: Overriding JIKE_API_BASE_URL can send requests to a different endpoint. <br>
Mitigation: Do not override JIKE_API_BASE_URL unless you control and trust the endpoint. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jikeapi-cn/jike-cookbook-query) <br>
- [JikeAPI homepage](https://www.jikeapi.cn/) <br>
- [JikeAPI cookbook search endpoint](https://api.jikeapi.cn/v1/cookbook/search) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Plain text tables and recipe details, or JSON when --json is used] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and JIKE_COOKBOOK_QUERY_KEY or JIKE_APPKEY; request URLs include the AppKey.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
