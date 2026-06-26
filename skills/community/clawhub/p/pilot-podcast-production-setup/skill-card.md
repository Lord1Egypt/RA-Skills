## Description: <br>
Deploy a podcast production pipeline with three agents for research, production, and distribution workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and podcast operations teams use this skill to configure a three-agent pipeline that turns topic research into show notes, episode packages, and distribution notifications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agent handshakes can create durable trust relationships with the wrong peer. <br>
Mitigation: Verify peer identities and hostnames out of band before handshakes, then inspect trust state before exchanging episode data. <br>
Risk: Distribution workflows can send episode metadata to RSS, podcast platforms, Slack, social channels, or webhooks. <br>
Mitigation: Use test or least-privilege credentials for external destinations and require human approval before publishing externally. <br>
Risk: Setup changes can persist through hostname, trust, and manifest state. <br>
Mitigation: Document rollback steps, including removing ~/.pilot/setups/podcast-production.json and resetting any pilotctl hostname or trust changes. <br>


## Reference(s): <br>
- [Pilot Protocol](https://pilotprotocol.network) <br>
- [ClawHub skill page](https://clawhub.ai/teoslayer/pilot-podcast-production-setup) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes role-specific setup manifests, hostname and handshake commands, subscription examples, and publishing examples.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
