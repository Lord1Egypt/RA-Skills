## Description: <br>
Queries a company API for the current list of available internal AI models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mcp98252302](https://clawhub.ai/user/mcp98252302) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees or developers use this skill in OpenClaw to check which internal AI models are currently available from the company API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts the disclosed company API domain to retrieve model data. <br>
Mitigation: Use it only in environments where contacting that domain is approved and the publisher is trusted. <br>
Risk: The model list depends on the availability and accuracy of the remote API response. <br>
Mitigation: Check for the returned error object before relying on the model list for operational decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mcp98252302/model-checker) <br>
- [Disclosed model list API endpoint](https://cwork-api-test.xgjktech.com.cn/filegpt/t_ai/nologin/aiTypeList) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON] <br>
**Output Format:** [API response data or an error object] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns the remote model-list response directly when the request succeeds.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
