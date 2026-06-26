## Description: <br>
Queries Jike's birthday flower API with an MM-DD birthday and returns the birthday flower, flower language, birthstone, and explanations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jikeapi-cn](https://clawhub.ai/user/jikeapi-cn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to answer traditional culture or lifestyle questions about birthday flowers, flower meanings, and birthstones from an MM-DD birthday. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The queried MM-DD birthday and Jike AppKey are sent to Jike's API. <br>
Mitigation: Use the skill only when that disclosure is acceptable, and prefer environment variables for the key instead of command-line arguments. <br>
Risk: Setting JIKE_API_BASE_URL can route requests to an alternate endpoint. <br>
Mitigation: Leave JIKE_API_BASE_URL unset unless the alternate endpoint is intentionally trusted. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jikeapi-cn/jike-birthday-flower-query) <br>
- [Jike API homepage](https://www.jikeapi.cn/) <br>
- [Birthday flower API endpoint](https://api.jikeapi.cn/v1/birthday/flower) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Chinese text summary by default, or JSON when --json is used] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and a JIKE_BIRTHDAY_FLOWER_QUERY_KEY or JIKE_APPKEY credential; accepts optional MM-DD birthday input.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
