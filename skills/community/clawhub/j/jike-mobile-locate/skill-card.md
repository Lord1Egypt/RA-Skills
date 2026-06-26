## Description: <br>
Looks up attribution details for 11-digit mainland China mobile numbers, including province, city, carrier, carrier type, area code, postal code, and administrative division code through the Jike API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jikeapi-cn](https://clawhub.ai/user/jikeapi-cn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and AI agents use this skill to answer mobile-number attribution questions for mainland China numbers. It returns masked human-readable results by default and can emit JSON for downstream processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queried phone numbers and the Jike AppKey are sent to a third-party API endpoint. <br>
Mitigation: Use the skill only for numbers you are authorized to query, and keep the AppKey out of public repositories, command histories, and shared logs. <br>
Risk: Changing JIKE_API_BASE_URL can route phone numbers and credentials to a non-default endpoint. <br>
Mitigation: Leave JIKE_API_BASE_URL unset unless you intentionally configure a trusted endpoint. <br>
Risk: The --no-mask option can expose full phone numbers in agent output. <br>
Mitigation: Use the default masked output unless full-number display is necessary and appropriate. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jikeapi-cn/jike-mobile-locate) <br>
- [Jike Data homepage](https://www.jikeapi.cn/) <br>
- [Jike mobile lookup API endpoint](https://api.jikeapi.cn/v1/mobile/query) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Masked human-readable text or JSON from a Python CLI script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and JIKE_MOBILE_KEY; default text output masks the middle four digits unless --no-mask is used.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
