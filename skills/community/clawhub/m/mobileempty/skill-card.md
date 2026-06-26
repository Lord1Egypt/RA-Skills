## Description: <br>
Checks batches of mobile phone numbers with JisuAPI and groups them as real, empty, unknown, or risk numbers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jisuapi](https://clawhub.ai/user/jisuapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to classify batches of mobile phone numbers as real, empty, unknown, or risky before cleanup, outreach, or review workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Target phone numbers are sent to JisuAPI using the user's API key. <br>
Mitigation: Use only numbers the user is authorized to process, protect the API key, and review JisuAPI privacy and retention terms before use. <br>
Risk: Phone-number classifications may be incomplete or unsuitable as the only basis for consequential decisions. <br>
Mitigation: Treat the result as one signal and apply human review or additional validation before marketing, fraud, eligibility, or similar decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jisuapi/mobileempty) <br>
- [JisuAPI](https://www.jisuapi.com/) <br>
- [JisuAPI mobile empty-number API](https://www.jisuapi.com/api/mobileempty/) <br>
- [JisuAPI mobileempty query endpoint](https://api.jisuapi.com/mobileempty/query) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [JSON from the helper script, usually summarized by the agent in Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, JISU_API_KEY, and a comma-separated mobiles string of up to 100 numbers.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
