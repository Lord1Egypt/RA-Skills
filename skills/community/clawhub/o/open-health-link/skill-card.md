## Description: <br>
Open Health Link connects an agent to breo Scalp5 health data so authorized users can bind or unbind a breo account, view scalp detection reports, and retrieve scalp care plans. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[breo](https://clawhub.ai/user/breo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill in OpenClaw to authorize access to their breo Scalp5 account, inspect recent scalp detection reports, review trends, and receive care-plan explanations based on available report data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive breo Scalp5 health report data. <br>
Mitigation: Use it only for an account the user intentionally authorizes, avoid exposing raw responses, and base report conclusions only on returned data. <br>
Risk: A local authorization token may remain in the skill directory until the account is unbound. <br>
Mitigation: Do not share the skill directory after use, and run the unbind flow when OpenClaw should no longer access the reports. <br>
Risk: First use requires installing Node.js dependencies for the skill scripts. <br>
Mitigation: Approve dependency installation only when the user trusts this release and intends to connect a breo Scalp5 account. <br>


## Reference(s): <br>
- [Open Health Link ClawHub page](https://clawhub.ai/breo/open-health-link) <br>
- [Publisher profile: breo](https://clawhub.ai/user/breo) <br>
- [Setup guide](assets/setup-guide.md) <br>
- [API reference](references/api-reference.md) <br>
- [Data schema](references/data-schema.md) <br>
- [Care-plan catalog data source](https://breo-obs.obs.cn-south-1.myhuaweicloud.com/agents/plan-catalog.csv) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and natural-language responses with occasional local image output for authorization QR codes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js at runtime and may use a local saved authorization token until the user unbinds the account.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
