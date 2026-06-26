## Description: <br>
Deploy a competitive intelligence system with 4 agents for crawling, analysis, tracking, and alerting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to set up a four-agent competitive intelligence workflow that crawls competitor sources, analyzes trends, tracks changes, and routes alerts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup routes competitive intelligence through peer messaging, Slack, and HTTPS webhooks. <br>
Mitigation: Use approved private channels and authenticated webhook endpoints, and avoid sending confidential strategy details unless necessary. <br>
Risk: The workflow changes local Pilot configuration, including hostnames and setup manifests. <br>
Mitigation: Verify the ~/.pilot manifest content and hostname changes before applying them. <br>
Risk: The setup depends on additional pilot-* skills and local binaries. <br>
Mitigation: Verify the required pilot-* dependency skills and the pilotctl and clawhub binaries before installation. <br>


## Reference(s): <br>
- [Pilot Protocol](https://pilotprotocol.network) <br>
- [ClawHub skill page](https://clawhub.ai/teoslayer/pilot-competitor-intelligence-setup) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces role-specific setup steps, manifests, peer handshakes, and example publish/subscribe commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
