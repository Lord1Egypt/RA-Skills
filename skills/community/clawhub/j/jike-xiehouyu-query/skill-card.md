## Description: <br>
查询或随机返回中文歇后语，并通过即刻数据（jikeapi.cn）接口提供结果。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jikeapi-cn](https://clawhub.ai/user/jikeapi-cn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and users working with Chinese language content use this skill to search xiehouyu by keyword or retrieve a random saying for explanation, recommendation, or writing support. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends xiehouyu search terms and the configured Jike API key to the API service. <br>
Mitigation: Avoid sensitive or private text, keep the API key scoped and protected, and install only when use of the Jike API service is acceptable. <br>
Risk: The JIKE_API_BASE_URL environment variable can route requests to an alternate endpoint. <br>
Mitigation: Leave JIKE_API_BASE_URL unset unless the alternate endpoint is intentionally configured and trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jikeapi-cn/jike-xiehouyu-query) <br>
- [Jike API homepage](https://www.jikeapi.cn/) <br>
- [Jike xiehouyu query API endpoint](https://api.jikeapi.cn/v1/xiehouyu/query) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration] <br>
**Output Format:** [Terminal table text or JSON from a Python command-line script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and a Jike API key via JIKE_XIEHOUYU_QUERY_KEY or JIKE_APPKEY.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
