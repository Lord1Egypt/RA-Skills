## Description: <br>
Queries an internal Kuaishou merchant CRM for seller IDs from a seller name using a local OpenClaw username. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jimadara](https://clawhub.ai/user/jimadara) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Authorized merchant operations or support users use this skill to resolve seller IDs from seller names through an internal Kuaishou CRM endpoint. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a local username to query an internal merchant CRM and may return raw seller IDs. <br>
Mitigation: Install and use only in authorized Kuaishou environments, verify the user is allowed to query the CRM system, and limit returned data. <br>
Risk: The skill is labeled as domain testing while its behavior is merchant CRM lookup. <br>
Mitigation: Rename and describe the skill accurately, and disclose local username access and the outbound request before installation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jimadara/intelligent-diagnosis-skill-test) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Text, JSON] <br>
**Output Format:** [Plain text or JSON-like HTTP response body returned from the merchant CRM lookup.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads ~/.openclaw/username; returns raw seller IDs or an authentication error.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata; artifact frontmatter reports 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
