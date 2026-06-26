## Description: <br>
Deploy an automated newsletter pipeline with three agents that curate content, write newsletter copy, and dispatch emails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure a three-agent newsletter automation workflow for content curation, drafting, and email delivery. It guides setup of role-specific skills, hostnames, trust handshakes, and message flows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Email dispatch can expose subscriber data or send messages to unintended recipients if configured against production lists too early. <br>
Mitigation: Test the workflow with sandbox or non-production recipient lists before enabling live delivery. <br>
Risk: The setup depends on downstream pilot-* skills and trusted host relationships. <br>
Mitigation: Review the downstream skills before installation and initiate handshakes only with trusted hosts. <br>
Risk: Newsletter delivery may involve consent, unsubscribe handling, credentials, and retention obligations. <br>
Mitigation: Confirm email-provider credentials, consent records, unsubscribe behavior, and retention rules before dispatching to subscribers. <br>


## Reference(s): <br>
- [Pilot Protocol](https://pilotprotocol.network) <br>
- [ClawHub release page](https://clawhub.ai/teoslayer/pilot-newsletter-automation-setup) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, json, guidance] <br>
**Output Format:** [Markdown with bash command examples and JSON configuration templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup guidance for role selection, skill installation, host naming, trust handshakes, manifests, subscriptions, and publish commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
