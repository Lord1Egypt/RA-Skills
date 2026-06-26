## Description: <br>
Queries JikeAPI for IPv6 location and carrier details, returning country, province, city, area, ISP, and long_ip values. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jikeapi-cn](https://clawhub.ai/user/jikeapi-cn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill when a user asks where an IPv6 address is located or which carrier operates it. It validates IPv6 input, calls the JikeAPI IPv6 lookup endpoint, and returns location and ISP details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queried IPv6 addresses and the Jike AppKey are sent to JikeAPI. <br>
Mitigation: Install only when this data sharing is acceptable, and prefer environment variables for the AppKey instead of command-line arguments on shared systems. <br>
Risk: A local scripts/.env file or custom JIKE_API_BASE_URL can expose secrets or route lookups to an unintended service. <br>
Mitigation: Do not commit scripts/.env, keep AppKeys out of source control, and leave JIKE_API_BASE_URL unset unless intentionally using a trusted replacement endpoint. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jikeapi-cn/jike-ip-query-v6) <br>
- [JikeAPI homepage](https://www.jikeapi.cn/) <br>
- [JikeAPI IPv6 lookup endpoint](https://api.jikeapi.cn/v1/ip/query/v6) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Plain text or JSON from a Python CLI command] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and a Jike AppKey via JIKE_IP_QUERY_V6_KEY or JIKE_APPKEY.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
