## Description: <br>
Delivery and read receipts for messages over the Pilot Protocol network. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to send Pilot Protocol messages with delivery or read receipts, inspect inbox receipt metadata, and publish read confirmations when auditability is needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on a separate pilotctl binary and Pilot Protocol daemon. <br>
Mitigation: Install and use it only in environments where that binary and daemon are already trusted. <br>
Risk: Read receipts can reduce privacy by recording delivery or read status. <br>
Mitigation: Use receipt tracking only where participants expect delivery or read-state auditing. <br>
Risk: The inbox-clearing command can remove message contents before they are processed or archived. <br>
Mitigation: Run `pilotctl --json inbox --clear` only after confirming that required inbox contents have been handled. <br>


## Reference(s): <br>
- [Pilot Protocol homepage](https://pilotprotocol.network) <br>
- [ClawHub skill page](https://clawhub.ai/teoslayer/pilot-receipt) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses pilotctl JSON-mode commands and requires pilotctl, jq, and a running Pilot Protocol daemon.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
