## Description: <br>
Human-friendly naming with aliases and namespaces for Pilot Protocol agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to register Pilot Protocol hostnames, resolve human-readable names to node IDs, look up node hostnames, and manage naming workflows for AI workers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on a local pilotctl binary and a running Pilot Protocol daemon. <br>
Mitigation: Install it only in environments where the Pilot Protocol daemon and pilotctl binary are trusted and expected. <br>
Risk: Hostname changes, peer listing, and connect examples perform user-directed network actions and may expose known agent metadata. <br>
Mitigation: Review command targets and outputs before running examples, especially in shared or sensitive agent networks. <br>


## Reference(s): <br>
- [Pilot Protocol](https://pilotprotocol.network) <br>
- [ClawHub listing](https://clawhub.ai/teoslayer/pilot-dns) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands use pilotctl JSON output and require the Pilot Protocol daemon to be running.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
