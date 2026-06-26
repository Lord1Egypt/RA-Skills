## Description: <br>
Deploy a brand protection system with four agents for scanning, classification, enforcement, and reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
AGPL-3.0 <br>


## Use Case: <br>
Developers and brand operations teams use this skill to configure a four-agent Pilot deployment for monitoring suspected counterfeits, classifying violations, coordinating enforcement actions, and reporting brand health. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can support takedown notices, platform reports, and cease-and-desist workflows that may affect external parties. <br>
Mitigation: Require human legal review and explicit scope approval before filing or sending any enforcement action. <br>
Risk: Brand evidence and status reports may be sent to external webhooks or Slack destinations. <br>
Mitigation: Verify every Pilot handshake and webhook or Slack destination before publishing reports or enforcement data. <br>
Risk: The deployment depends on Pilot skills, pilotctl, clawhub, and a running daemon. <br>
Mitigation: Pin and review the dependent Pilot skills and confirm the runtime components before installation. <br>


## Reference(s): <br>
- [Pilot Protocol homepage](https://pilotprotocol.network) <br>
- [ClawHub skill page](https://clawhub.ai/teoslayer/pilot-brand-protection-setup) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON manifest templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes role-specific setup manifests, hostnames, handshakes, and data-flow examples.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
