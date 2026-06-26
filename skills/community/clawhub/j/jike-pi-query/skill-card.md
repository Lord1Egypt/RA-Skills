## Description: <br>
支持查找圆周率指定位置开始的数字，也支持查找指定数字在圆周率中的位置。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jikeapi-cn](https://clawhub.ai/user/jikeapi-cn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to look up digits of pi from a starting position or find where a digit sequence appears in pi through Jike's API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends requests to an external Jike API and requires an API key. <br>
Mitigation: Install only when Jike API access is intended, keep the key in environment variables, and avoid exposing command output that includes credentials. <br>
Risk: The JIKE_API_BASE_URL override can redirect requests to a different endpoint. <br>
Mitigation: Leave JIKE_API_BASE_URL unset unless the endpoint is trusted and explicitly approved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jikeapi-cn/jike-pi-query) <br>
- [Publisher profile](https://clawhub.ai/user/jikeapi-cn) <br>
- [Jike API homepage](https://www.jikeapi.cn/) <br>
- [Pi lookup API endpoint](https://api.jikeapi.cn/v1/pi/find_number) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Plain text or JSON returned by a Python command-line script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and a JIKE_PI_QUERY_KEY or JIKE_APPKEY credential; optional JSON output is available with --json.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
