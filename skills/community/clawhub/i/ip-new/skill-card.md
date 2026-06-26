## Description: <br>
聚合数据IP归属地查询V3.0，支持IPv4查询国家/省份/城市/运营商。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[365bug](https://clawhub.ai/user/365bug) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to query IPv4 ownership details from Juhe, including country, province, city, and carrier information. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The implementation sends JUHE_API_KEY and queried IP addresses over plain HTTP. <br>
Mitigation: Use only after reviewing the endpoint behavior, prefer HTTPS before deployment, and rotate any key already used with the current HTTP implementation. <br>
Risk: The skill depends on an external Juhe API and a configured JUHE_API_KEY. <br>
Mitigation: Configure the API key through the environment and treat API errors or unavailable network access as expected operational failure modes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/365bug/ip-new) <br>
- [Juhe IP lookup endpoint](http://apis.juhe.cn/ip/ipNewV3) <br>
- [Publisher profile](https://clawhub.ai/user/365bug) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Shell commands, Configuration] <br>
**Output Format:** [JSON response printed to standard output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, the requests package, and JUHE_API_KEY.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
