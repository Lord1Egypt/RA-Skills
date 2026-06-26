## Description: <br>
根据身份证号解析地区、出生日期、性别与校验位；可按城市查前六位规则。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jisuapi](https://clawhub.ai/user/jisuapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to look up Chinese ID card origin details, birth date, sex, and checksum status, or to find the first six ID-card digits for a city. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Full national ID numbers may be sent to JisuAPI during lookup. <br>
Mitigation: Submit full ID numbers only with authorization and a clear need; use a six-digit prefix or city lookup when sufficient. <br>
Risk: The skill requires a JISU_API_KEY credential. <br>
Mitigation: Keep the API key private, store it in the environment, and avoid exposing it in prompts, logs, or shared outputs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jisuapi/idcard) <br>
- [JisuAPI home](https://www.jisuapi.com/) <br>
- [JisuAPI ID card lookup documentation](https://www.jisuapi.com/api/idcard/) <br>
- [JisuAPI ID card query endpoint](https://api.jisuapi.com/idcard/query) <br>
- [JisuAPI city-to-code endpoint](https://api.jisuapi.com/idcard/city2code) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, JSON, Guidance] <br>
**Output Format:** [JSON responses with concise natural-language guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and JISU_API_KEY; calls JisuAPI endpoints for lookup results.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
