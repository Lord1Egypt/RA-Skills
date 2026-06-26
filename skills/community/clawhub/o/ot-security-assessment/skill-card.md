## Description: <br>
Assess OT/ICS security posture across 30 controls in 6 principles: Business Driven, Risk Based, Enterprise Wide, Methodical, OT Security Focused, and OT Security Compliant. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security practitioners, OT engineers, and operators use this skill to collect control-level OT/ICS security posture inputs and produce a scored assessment with gaps, risk level, and prioritized remediation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: OT/ICS assessment inputs may contain sensitive operational or critical-infrastructure details when sent to the ToolWeb API. <br>
Mitigation: Use a dedicated API key, avoid facility-identifying or highly detailed production data unless necessary, and confirm ToolWeb retention and privacy practices before real-world use. <br>
Risk: The skill depends on an external API and API key, so assessments may fail if the key is missing, invalid, rate-limited, or the service is unavailable. <br>
Mitigation: Verify TOOLWEB_API_KEY and curl before use, handle API errors explicitly, and retry only according to the service limits. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/krishnakumarmahadevan-cmd/ot-security-assessment) <br>
- [ToolWeb API portal](https://portal.toolweb.in) <br>
- [OT Security Assessment API endpoint](https://portal.toolweb.in/apis/security/ot-security-assessment) <br>
- [ToolWeb platform](https://toolweb.in) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown text with compliance scores, risk level, findings, and remediation guidance; may include shell commands for API execution and configuration.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TOOLWEB_API_KEY and curl; successful use sends assessment inputs to the ToolWeb API.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
