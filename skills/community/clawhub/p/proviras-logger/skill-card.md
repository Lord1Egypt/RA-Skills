## Description: <br>
Run on every heartbeat to summarize completed tasks and log them to a Proviras analytics dashboard. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[proviras](https://clawhub.ai/user/proviras) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agent users and operators use this skill to record heartbeat-based task activity, model identifiers, skill usage, and agent relationships in a Proviras analytics dashboard. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Continuous heartbeat logging sends identifiable agent and task data to Proviras. <br>
Mitigation: Install and enable the skill only where users have approved continuous analytics collection for the affected agents and tasks. <br>
Risk: Parent and child agents can be persistently linked when Proviras environment variables are propagated. <br>
Mitigation: Do not pass PROVIRAS_PARENT_ID or PROVIRAS_USER_ID to sub-agents unless all affected users have approved that tracking. <br>
Risk: The skill has no built-in consent gate for cross-agent tracking. <br>
Mitigation: Manage consent and environment-variable propagation outside the skill before deployment. <br>


## Reference(s): <br>
- [Proviras Logger ClawHub Page](https://clawhub.ai/proviras/proviras-logger) <br>
- [proviras Publisher Profile](https://clawhub.ai/user/proviras) <br>
- [Payload Schema](references/payload-schema.md) <br>
- [Configuration Reference](references/config.md) <br>
- [Proviras Service](https://proviras.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration] <br>
**Output Format:** [Heartbeat status text plus JSON payloads submitted by shell scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads session memory and local agent configuration, then submits heartbeat and registration data to Proviras.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
