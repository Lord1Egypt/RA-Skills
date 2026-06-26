## Description: <br>
国内猪肉价格实时查询。按省份查询白条肉、精瘦肉、土杂猪、外三元、内三元价格，也支持不传省份返回全部地区价格。适用场景：用户说“四川今天猪肉价格多少”“查一下广东精瘦肉价格”“全国猪肉价格列表”等。数据由即刻数据（jikeapi.cn）开放接口提供。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jikeapi-cn](https://clawhub.ai/user/jikeapi-cn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to query current pork prices in China by province or nationwide, then return prices for carcass pork, lean pork, native pigs, three-way hybrid pigs, and three-line hybrid pigs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends pork-price lookup requests and an API key to Jike's API. <br>
Mitigation: Use a dedicated low-privilege Jike API key and avoid sharing logs or full request URLs that contain appkey values. <br>
Risk: The script can redirect requests when JIKE_API_BASE_URL is set. <br>
Mitigation: Leave JIKE_API_BASE_URL unset unless intentionally routing requests to a trusted endpoint. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jikeapi-cn/jike-pork-query) <br>
- [Jike API homepage](https://www.jikeapi.cn/) <br>
- [Jike pork query API endpoint](https://api.jikeapi.cn/v1/pork/query) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Terminal table text or JSON payload, with agent-facing Markdown guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and a Jike API key provided through JIKE_PORK_QUERY_KEY, JIKE_APPKEY, or --key.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
