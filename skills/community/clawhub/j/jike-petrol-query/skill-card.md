## Description: <br>
Queries current China domestic prices for 92, 95, and 98 octane gasoline and 0 diesel by province or nationwide using the Jike Data API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jikeapi-cn](https://clawhub.ai/user/jikeapi-cn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and AI clients use this skill to answer fuel-price questions such as a province-specific gasoline price or a nationwide oil price list. It returns current price fields for 92, 95, and 98 octane gasoline and 0 diesel. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A Jike API key is required and could be exposed if passed on the command line or captured in logged request URLs. <br>
Mitigation: Prefer JIKE_PETROL_QUERY_KEY in the environment, avoid using --key for routine use, and do not log full request URLs. <br>
Risk: The skill performs outbound requests to the Jike petrol-price API. <br>
Mitigation: Install and run it only where outbound access to the Jike API and use of a Jike API key are acceptable. <br>
Risk: JIKE_API_BASE_URL can redirect requests to a different endpoint if set. <br>
Mitigation: Keep JIKE_API_BASE_URL unset unless deliberately testing against a trusted endpoint. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jikeapi-cn/jike-petrol-query) <br>
- [Jike Data homepage](https://www.jikeapi.cn/) <br>
- [Jike petrol query API endpoint](https://api.jikeapi.cn/v1/petrol/query) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, API Calls] <br>
**Output Format:** [Terminal table text or JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Jike API key from JIKE_PETROL_QUERY_KEY or JIKE_APPKEY and outbound access to api.jikeapi.cn.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
