## Description: <br>
Reports comprehensive Pilot Protocol mesh status across peers, connections, encryption, relay usage, bandwidth, and daemon health. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators using Pilot Protocol use this skill to generate mesh status reports for network health monitoring, dashboard inputs, and connectivity or performance debugging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Mesh status reports can expose operational details such as node IDs, peers, connection patterns, relay use, bandwidth, and encryption coverage. <br>
Mitigation: Share generated reports only with trusted operators and redact sensitive mesh details before storing or publishing them. <br>
Risk: The skill relies on the local pilotctl binary and daemon for status data. <br>
Mitigation: Use it only in a trusted Pilot Protocol environment where the pilotctl binary and daemon are expected and maintained. <br>


## Reference(s): <br>
- [Pilot Protocol homepage](https://pilotprotocol.network) <br>
- [ClawHub skill page](https://clawhub.ai/teoslayer/pilot-mesh-status) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with pilotctl command examples, JSON-oriented command output expectations, and bash snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the pilotctl binary on PATH and a running Pilot Protocol daemon; reports may include node IDs, peer and connection details, relay use, bandwidth, and encryption coverage.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; artifact metadata version 1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
