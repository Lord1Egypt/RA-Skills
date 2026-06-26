## Description: <br>
查企业工商基本信息、名称搜索、变更与股东高管等。当用户说：查一下某某公司的注册资本、法人是谁？企业变更记录，或类似工商信息问题时，使用本技能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jisuapi](https://clawhub.ai/user/jisuapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to query JisuAPI for Chinese enterprise registration details, company-name search results, change records, shareholder information, and executive information. It is suited to user-facing business information lookups where disclosing the searched company name or identifier to JisuAPI is acceptable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Company names, registration numbers, credit codes, or organization codes are sent to JisuAPI during lookup. <br>
Mitigation: Use the skill only when third-party disclosure to JisuAPI is acceptable, and avoid submitting confidential research targets. <br>
Risk: The skill depends on a JisuAPI AppKey that may have quota, permission, expiration, or IP restrictions. <br>
Mitigation: Use a dedicated, quota-limited JISU_API_KEY where possible and handle API error JSON before relying on results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jisuapi/jisu-enterprise) <br>
- [JisuAPI enterprise API documentation](https://www.jisuapi.com/api/enterprise/) <br>
- [JisuAPI provider site](https://www.jisuapi.com/) <br>
- [JisuAPI enterprise endpoint](https://api.jisuapi.com/enterprise) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON results and Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and a JISU_API_KEY environment variable. API requests are read-only and may return enterprise basic information, search results, change records, shareholder data, executive data, or structured error JSON.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
