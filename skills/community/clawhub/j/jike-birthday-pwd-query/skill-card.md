## Description: <br>
生日密码。输入 MM-DD 生日，查询幸运、健康、建议、名人、塔罗、箴言、优点和缺点。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jikeapi-cn](https://clawhub.ai/user/jikeapi-cn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent builders use this skill to query birthday-password information from the Jike API when a user provides an MM-DD birthday value. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Birthday input and the configured API key are sent to the third-party service at api.jikeapi.cn. <br>
Mitigation: Use the skill only for explicit birthday-password lookups and only when that data sharing is acceptable. <br>
Risk: The API credential could be overprivileged or reused across services. <br>
Mitigation: Configure a dedicated low-privilege API key through JIKE_BIRTHDAY_PWD_QUERY_KEY or JIKE_APPKEY. <br>
Risk: A custom API base URL can redirect requests away from the default Jike API endpoint. <br>
Mitigation: Avoid setting JIKE_API_BASE_URL unless the endpoint is controlled and trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jikeapi-cn/jike-birthday-pwd-query) <br>
- [Jike API homepage](https://www.jikeapi.cn/) <br>
- [Birthday password API endpoint](https://api.jikeapi.cn/v1/birthday/pwd) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, API calls, guidance] <br>
**Output Format:** [Chinese text summary or JSON API response] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and a JIKE_BIRTHDAY_PWD_QUERY_KEY or JIKE_APPKEY credential.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
