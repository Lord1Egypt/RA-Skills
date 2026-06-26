## Description: <br>
Checks a JisuAI account balance and remaining call count by reading the configured API key and calling the JisuAI balance API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[outRice](https://clawhub.ai/user/outRice) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query their JisuAI account balance and remaining usage count from an existing OpenClaw configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads a JisuAI API key from the local OpenClaw configuration. <br>
Mitigation: Review the skill before installing and only run it when you are comfortable granting it access to that configured credential. <br>
Risk: The skill sends the API key to a plain HTTP balance endpoint using a query-string parameter. <br>
Mitigation: Prefer a version that uses HTTPS and avoids placing secrets in URLs before using it with sensitive or production credentials. <br>


## Reference(s): <br>
- [JisuAI provider base URL](https://v2.aicodee.com) <br>
- [JisuAI balance API endpoint](http://v2api.aicodee.com/chaxun/balance) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text status message] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns balance, remaining call count, or a localized error message depending on the query and API response.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
