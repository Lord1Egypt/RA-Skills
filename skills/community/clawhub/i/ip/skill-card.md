## Description: <br>
根据 IP 查归属地与运营商类型。当用户说：这个 IP 是哪里的？是不是机房 IP？或类似 IP 归属问题时，使用本技能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jisuapi](https://clawhub.ai/user/jisuapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to look up an IP address and summarize its location and operator type using JisuAPI data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queried IP addresses are sent to JisuAPI. <br>
Mitigation: Avoid querying confidential internal, customer, or security-sensitive IP addresses unless sharing them with JisuAPI is acceptable for the environment. <br>
Risk: The skill requires a JisuAPI key. <br>
Mitigation: Provide JISU_API_KEY through the agent environment and avoid exposing it in prompts, logs, or shared command examples. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jisuapi/ip) <br>
- [JisuAPI](https://www.jisuapi.com/) <br>
- [JisuAPI IP query documentation](https://www.jisuapi.com/api/ip/) <br>
- [JisuAPI IP location endpoint](https://api.jisuapi.com/ip/location) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, API Calls, Shell commands, Configuration guidance] <br>
**Output Format:** [JSON returned by a Python command-line script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and the JISU_API_KEY environment variable; queried IP addresses are sent to JisuAPI.] <br>

## Skill Version(s): <br>
1.0.2 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
