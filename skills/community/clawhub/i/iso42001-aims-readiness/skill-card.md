## Description: <br>
Assess ISO/IEC 42001:2023 AI Management System (AIMS) readiness and generate compliance gap analysis with remediation roadmap. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and governance teams use this skill to collect AI governance details, call the ToolWeb API, and receive ISO/IEC 42001 readiness scoring, gap analysis, and remediation guidance for certification preparation and related AI governance work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends organizational AI governance and compliance details to ToolWeb. <br>
Mitigation: Use only with approval for the data being submitted, and avoid regulated, confidential, or sensitive organizational details unless the organization's policy permits it. <br>
Risk: The bundled test script uses curl with TLS verification disabled. <br>
Mitigation: Do not run scripts/test-api.sh as-is; remove the -k option before using the script against the API. <br>
Risk: The security verdict is suspicious because the skill depends on an external API and weakens API-key protection in the test script. <br>
Mitigation: Review the skill before installation, validate the API destination, scope the API key, and rotate credentials if they may have been exposed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/krishnakumarmahadevan-cmd/iso42001-aims-readiness) <br>
- [ToolWeb Platform](https://toolweb.in) <br>
- [ToolWeb API Hub](https://portal.toolweb.in) <br>
- [ISO 42001 API Endpoint](https://portal.toolweb.in/apis/iso42001) <br>
- [OpenClaw Skills](https://toolweb.in/openclaw/) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Markdown, Guidance] <br>
**Output Format:** [Markdown assessment report based on a JSON API response] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TOOLWEB_API_KEY and curl; successful API calls may be metered by the provider.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
