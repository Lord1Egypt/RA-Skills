## Description: <br>
Looks up merchant seller IDs from a parsed merchant name by using a local OpenClaw username and returning the merchant service response. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jimadara](https://clawhub.ai/user/jimadara) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Authorized internal users can ask the agent to parse a merchant name and query the merchant CRM seller search endpoint for matching seller IDs. The skill should be treated as a merchant lookup helper rather than a domain-testing or diagnosis-report generator. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release is presented as domain testing or diagnosis reporting, but the security review says it performs internal merchant lookup. <br>
Mitigation: Review the skill purpose before installing and update the public name and description so users understand it queries merchant seller data. <br>
Risk: The skill reads a local OpenClaw username and sends it with the merchant name to an internal merchant CRM endpoint. <br>
Mitigation: Install only for users authorized to query that endpoint, and disclose the local username requirement before use. <br>
Risk: The skill returns raw internal API responses, which may expose more operational detail than users need. <br>
Mitigation: Review returned data before sharing it and prefer a constrained, user-confirmed output format for production use. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, API calls, Guidance] <br>
**Output Format:** [Raw service response, typically JSON-like text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns the HTTP interface result directly to the user.] <br>

## Skill Version(s): <br>
1.0.12 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
