## Description: <br>
Deploys a three-agent proposal writing system for researching RFP requirements, drafting proposal sections, and reviewing submissions for compliance and win themes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and proposal operations teams use this skill to configure a coordinated research, drafting, and review pipeline for RFP responses and proposal submissions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can send final proposal data to an external webhook endpoint. <br>
Mitigation: Configure only destinations you control and require deliberate approval before external submission. <br>
Risk: Setup depends on pilotctl, clawhub, and related Pilot bridge skills. <br>
Mitigation: Verify binaries and bridge skills come from trusted sources before installation. <br>
Risk: Proposal drafts may contain sensitive business data. <br>
Mitigation: Test with non-sensitive data first and avoid using confidential proposal content until the deployment is verified. <br>


## Reference(s): <br>
- [Pilot Protocol](https://pilotprotocol.network) <br>
- [ClawHub skill page](https://clawhub.ai/teoslayer/pilot-proposal-writer-setup) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces role-specific setup steps, hostnames, manifests, handshakes, subscriptions, and publish examples.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
