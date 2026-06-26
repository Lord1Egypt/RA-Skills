## Description: <br>
星座配对。输入男生星座和女生星座，查询配对指数、比例、同情指数、天长地久指数、结果评述和恋爱建议。适用场景：用户询问相关传统文化、生活常识或配对资料时使用。数据由即刻数据（jikeapi.cn）开放接口提供。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jikeapi-cn](https://clawhub.ai/user/jikeapi-cn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to query Jike Data for Chinese zodiac-sign compatibility details, including compatibility index, proportions, empathy index, longevity index, assessment, and dating advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends the two zodiac signs and a Jike API key to Jike's API. <br>
Mitigation: Use a dedicated, revocable Jike API key and only run the skill when sharing those query values with Jike is acceptable. <br>
Risk: Supplying the API key with the command-line --key option may expose it through shell history or process listings on shared systems. <br>
Mitigation: Prefer environment variables such as JIKE_ZODIAC_PAIRING_QUERY_KEY or JIKE_APPKEY instead of passing the key as a command-line argument. <br>
Risk: Overriding JIKE_API_BASE_URL can redirect requests to a different endpoint. <br>
Mitigation: Leave JIKE_API_BASE_URL unset unless a trusted alternate endpoint is intentionally required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jikeapi-cn/jike-zodiac-pairing-query) <br>
- [Jike Data homepage](https://www.jikeapi.cn/) <br>
- [Jike zodiac pairing API endpoint](https://api.jikeapi.cn/v1/zodiac_pairing) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, API calls, Guidance] <br>
**Output Format:** [Chinese plain text by default, or JSON when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and a Jike API key supplied through JIKE_ZODIAC_PAIRING_QUERY_KEY or JIKE_APPKEY.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
