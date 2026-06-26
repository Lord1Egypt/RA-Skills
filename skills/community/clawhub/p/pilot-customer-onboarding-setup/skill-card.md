## Description: <br>
Deploy a customer onboarding system with three agents that automate the new customer journey from welcome through setup to success tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and customer success teams use this skill to set up a three-agent Pilot Protocol onboarding workflow with a welcome bot, setup guide, and success tracker. It helps install role-specific skills, configure hostnames, create setup manifests, establish peer trust, and test customer onboarding data flows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Customer onboarding, health, and alert data may be sent to Slack, webhooks, dashboards, or peer agents. <br>
Mitigation: Confirm which customer fields are shared, avoid unnecessary PII, and apply consent, retention, and access-control rules before deployment. <br>
Risk: Webhook or Slack integrations may expose onboarding data if credentials are broad or unmanaged. <br>
Mitigation: Use least-privilege webhook credentials and rotate or revoke them when access changes. <br>
Risk: The workflow depends on role-specific Pilot Protocol skills, pilotctl, clawhub, and a running daemon. <br>
Mitigation: Verify prerequisites and peer handshakes before using the workflow with live customer data. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/teoslayer/pilot-customer-onboarding-setup) <br>
- [Pilot Protocol homepage](https://pilotprotocol.network) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces role-specific setup instructions, setup manifest templates, peer handshake commands, and workflow test commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
