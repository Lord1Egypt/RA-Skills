## Description: <br>
Deploy a video production pipeline with three agents that automate script writing, editing coordination, and multi-platform distribution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content operations teams use this skill to configure three coordinated Pilot Protocol agents for script writing, video editing coordination, and distribution. It helps set hostnames, install role-specific skills, create a setup manifest, and establish trusted agent handshakes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup installs multiple downstream pilot-* skills and depends on pilotctl and clawhub. <br>
Mitigation: Confirm you trust the publisher, pilotctl, clawhub, and each downstream skill before allowing install commands. <br>
Risk: Agent handshakes establish trusted communication paths for script, edited-video, and publish-notification data flows. <br>
Mitigation: Only handshake with verified agents you control, and review the target hostnames and topics before subscribing or publishing. <br>
Risk: The setup writes a persistent manifest under ~/.pilot/setups for the video production pipeline. <br>
Mitigation: Review the manifest after setup and delete it when the workflow is no longer needed. <br>


## Reference(s): <br>
- [Pilot Protocol homepage](https://pilotprotocol.network) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces role-specific setup instructions and manifest content for a three-agent video production workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
