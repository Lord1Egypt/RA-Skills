## Description: <br>
生肖查询可按生肖名称查询五行、本命佛、出生年份、幸运数字、幸运花、性格、事业、爱情和运势，适用于用户询问相关传统文化、生活常识或配对资料的场景，数据由即刻数据（jikeapi.cn）开放接口提供。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jikeapi-cn](https://clawhub.ai/user/jikeapi-cn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to query Chinese zodiac reference data from Jike API, including elements, natal Buddha, birth years, lucky numbers, flowers, personality notes, career, love, health, fortune, and compatibility information. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends lookup requests to jikeapi.cn using a user-provided Jike API key. <br>
Mitigation: Install and use it only when the user trusts jikeapi.cn and is comfortable using that API key for this lookup. <br>
Risk: Passing a real key with --key can expose credentials in shared command transcripts or shell history. <br>
Mitigation: Prefer JIKE_CHINESE_ZODIAC_QUERY_KEY or JIKE_APPKEY environment variables for normal use. <br>
Risk: JIKE_API_BASE_URL can redirect API calls away from the default endpoint if set. <br>
Mitigation: Leave JIKE_API_BASE_URL unset unless the user intentionally wants to change the API endpoint. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jikeapi-cn/jike-chinese-zodiac-query) <br>
- [Jike API homepage](https://www.jikeapi.cn/) <br>
- [Chinese zodiac API endpoint](https://api.jikeapi.cn/v1/chinese_zodiac) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [Chinese plain text by default, or JSON when invoked with --json] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and a Jike API key supplied through JIKE_CHINESE_ZODIAC_QUERY_KEY or JIKE_APPKEY.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
