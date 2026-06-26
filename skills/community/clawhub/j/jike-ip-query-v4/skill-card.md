## Description: <br>
输入 IPv4 地址，实时查询国家、省份、城市、运营商和 long_ip 数值。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jikeapi-cn](https://clawhub.ai/user/jikeapi-cn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, AI clients, and end users use this skill to look up IPv4 geolocation and carrier information from a Jike API response. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queried IPv4 addresses and the configured Jike API key are sent to Jike's API service. <br>
Mitigation: Use the skill only when sharing that lookup data with Jike is acceptable, and keep API keys in environment variables rather than public repositories or shared skill packages. <br>
Risk: Changing JIKE_API_BASE_URL can redirect lookups and credentials to an alternate endpoint. <br>
Mitigation: Set JIKE_API_BASE_URL only when the alternate endpoint is intentionally trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jikeapi-cn/jike-ip-query-v4) <br>
- [即刻数据 homepage](https://www.jikeapi.cn/) <br>
- [即刻数据 IPv4 query API](https://api.jikeapi.cn/v1/ip/query/v4) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text or JSON returned by a Python command-line script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and a JIKE_IP_QUERY_V4_KEY or JIKE_APPKEY credential.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
