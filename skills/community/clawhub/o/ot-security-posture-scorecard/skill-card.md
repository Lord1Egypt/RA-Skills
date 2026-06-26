## Description: <br>
Assess OT/ICS/SCADA security posture and generate risk scorecards with remediation guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security practitioners, OT operators, and critical-infrastructure teams use this skill to collect OT environment details, request a ToolWeb assessment, and review a posture scorecard with risk ratings, framework mapping, and remediation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive OT/ICS/SCADA posture details are sent to a third-party ToolWeb service. <br>
Mitigation: Use only with organizational approval, and minimize or anonymize organization names, plant details, known gaps, and threat concerns before submission. <br>
Risk: The ToolWeb API key may be exposed if copied into chat logs, scripts, or shared configuration. <br>
Mitigation: Store TOOLWEB_API_KEY in the agent environment or a secrets manager and rotate it if exposure is suspected. <br>
Risk: The included test script uses curl with TLS certificate verification disabled. <br>
Mitigation: Do not run scripts/test-api.sh unless curl -k is removed or a trusted certificate setup is used. <br>
Risk: Automated scorecards can be incomplete or misleading for safety-critical OT environments. <br>
Mitigation: Have qualified security and OT personnel review findings before making operational or control-system changes. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/krishnakumarmahadevan-cmd/ot-security-posture-scorecard) <br>
- [ToolWeb API portal](https://portal.toolweb.in) <br>
- [ToolWeb platform](https://toolweb.in) <br>
- [ToolWeb OpenClaw skills](https://toolweb.in/openclaw/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown scorecard with summarized assessment results and remediation steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TOOLWEB_API_KEY and curl; sends the assessment request to the ToolWeb API.] <br>

## Skill Version(s): <br>
1.3.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
