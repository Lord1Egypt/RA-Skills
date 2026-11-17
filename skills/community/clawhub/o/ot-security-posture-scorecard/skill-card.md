## Description:

Assess OT/ICS/SCADA security posture and generate risk scorecards with remediation guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

Security teams, OT engineers, and compliance practitioners use this skill to collect OT environment details, submit them to the ToolWeb.in assessment API, and receive a scorecard with risk ratings, framework mapping, and remediation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends OT/ICS environment details to a third-party ToolWeb.in service.

Mitigation: Use sanitized, non-sensitive details unless organizational policy approves sharing the data with ToolWeb.in and retention/privacy terms have been reviewed.

Risk: The bundled test script disables TLS certificate verification.

Mitigation: Do not run scripts/test-api.sh until TLS verification is restored by removing the -k option from curl.

Risk: TOOLWEB_API_KEY is used to authenticate assessment API calls.

Mitigation: Store the API key as a secret, avoid exposing it in logs or shared configuration, and rotate it if it may have crossed an untrusted network.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/krishnakumarmahadevan-cmd/skills/ot-security-posture-scorecard)
- [ToolWeb.in platform](https://toolweb.in)
- [ToolWeb.in API portal](https://portal.toolweb.in)
- [OT assessment API endpoint](https://portal.toolweb.in:8443/security/itotassessor)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown scorecard with summarized assessment results, risk ratings, and remediation guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TOOLWEB_API_KEY and curl; assessment requests are sent to a third-party ToolWeb.in API.]

## Skill Version(s):

1.3.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
