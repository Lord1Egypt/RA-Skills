## Description: <br>
Perform comprehensive IT risk assessments across infrastructure, data protection, access control, compliance, incident response, and vendor management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security teams, IT risk owners, and audit stakeholders use this skill to collect security-control maturity inputs, call ToolWeb's assessment API, and present an overall risk score, domain breakdown, critical gaps, and prioritized remediation roadmap. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive organizational security posture details may be sent to the external ToolWeb service. <br>
Mitigation: Avoid submitting secrets, exact internal hostnames, customer data, unreleased incidents, or highly specific vulnerabilities unless approved for ToolWeb processing and retention. <br>
Risk: The workflow depends on an external API key and tracked ToolWeb API usage. <br>
Mitigation: Confirm TOOLWEB_API_KEY access, billing expectations, and retry behavior before using the skill in production workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/krishnakumarmahadevan-cmd/it-risk-assessment-tool) <br>
- [ToolWeb API portal](https://portal.toolweb.in) <br>
- [IT risk assessment API endpoint](https://portal.toolweb.in/apis/security/it-risk-assessment) <br>
- [ToolWeb platform](https://toolweb.in) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown report with an overall risk score, domain scores, critical gaps, and prioritized remediation actions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TOOLWEB_API_KEY and curl; submits control maturity inputs to the ToolWeb API.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
