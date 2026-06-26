## Description: <br>
Peer review system for task results before acceptance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
AGPL-3.0 <br>


## Use Case: <br>
Developers and operators use this skill to request independent review of task results, collect approvals, and decide whether critical outputs should be accepted. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review requests and responses pass through external Pilot service agents and may expose private task details or sensitive business context. <br>
Mitigation: Use only with a trusted pilotctl and daemon setup, and avoid sending secrets or sensitive task context in lookup messages. <br>


## Reference(s): <br>
- [Pilot Protocol homepage](https://pilotprotocol.network) <br>
- [ClawHub skill listing](https://clawhub.ai/teoslayer/pilot-review) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, JSON messages] <br>
**Output Format:** [Markdown with bash code blocks and JSON message payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires pilot-protocol, pilotctl on PATH, a running pilotctl daemon, and jq.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
