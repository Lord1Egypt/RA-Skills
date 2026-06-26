## Description: <br>
Deploys a three-agent Pilot Protocol workflow for planning social media content, preparing platform-specific posts, and feeding performance insights back into future planning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to set up a Pilot Protocol social media management workflow across planner, creator, and analyst agents. It guides installation of role-specific skills, hostnames, setup manifests, handshakes, subscriptions, and example message flows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup changes local Pilot state, hostnames, and trust relationships that persist after the session. <br>
Mitigation: Install only on hosts intended for this workflow, use a trusted hostname prefix, and review ~/.pilot setup state and trust entries after configuration. <br>
Risk: The workflow can support social media posting automation and may interact with external social media accounts through installed role skills. <br>
Mitigation: Review the installed pilot-* skills and account permissions before granting posting, scheduling, analytics, or automation authority. <br>


## Reference(s): <br>
- [Pilot Protocol](https://pilotprotocol.network) <br>
- [ClawHub release page](https://clawhub.ai/teoslayer/pilot-social-media-manager-setup) <br>
- [Publisher profile](https://clawhub.ai/user/teoslayer) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces role-specific setup instructions and local Pilot manifest content for planner, creator, or analyst agents.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
