## Description: <br>
Multi-agent event aggregation on shared topics for coordinated workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
AGPL-3.0 <br>


## Use Case: <br>
Developers and agent operators use this skill to publish, subscribe to, and inspect shared Pilot Protocol topics for broadcast coordination and fleet state changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Events published to shared topics may expose sensitive data to subscribed trusted agents. <br>
Mitigation: Avoid secrets and credentials in event payloads and publish only data suitable for the trusted subscribers on the topic. <br>
Risk: Broad or wildcard topic subscriptions can distribute events more widely than intended. <br>
Mitigation: Prefer narrow topic names, review forwarding rules before use, and confirm mutual trust before coordinating agents. <br>


## Reference(s): <br>
- [Pilot Protocol](https://pilotprotocol.network) <br>
- [ClawHub skill listing](https://clawhub.ai/teoslayer/pilot-event-bus) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses JSON output from pilotctl commands when examples are executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
