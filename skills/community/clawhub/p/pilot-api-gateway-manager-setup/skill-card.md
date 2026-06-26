## Description: <br>
Deploys an API gateway management setup with four Pilot agents for service discovery, request routing, authentication, and monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and infrastructure engineers use this skill to configure a Pilot-based API gateway across discovery, router, auth, and monitor agents. It helps set hostnames, install role-specific skills, write role manifests, and establish trusted peer handshakes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup handles peer trust, API authentication examples, access logs, and role manifests that may contain sensitive operational details. <br>
Mitigation: Review ~/.pilot/setups/api-gateway-manager.json before writing it, use test or redacted credentials in examples, and confirm every peer hostname is controlled by the operator. <br>
Risk: The workflow installs downstream pilot-* skills and depends on pilotctl and clawhub binaries. <br>
Mitigation: Vet the downstream skills and required binaries before enabling the gateway setup in an operational environment. <br>
Risk: The monitor role can send API alerts to external dashboards or Slack. <br>
Mitigation: Enable external alerting only after confirming destinations, credentials, and shared alert contents are approved for the deployment. <br>


## Reference(s): <br>
- [Pilot Protocol homepage](https://pilotprotocol.network) <br>
- [ClawHub skill page](https://clawhub.ai/teoslayer/pilot-api-gateway-manager-setup) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash command blocks and JSON manifest templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Role-specific setup guidance for four Pilot API gateway agents; requires pilotctl, clawhub, Pilot Protocol skills, and a running daemon.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
