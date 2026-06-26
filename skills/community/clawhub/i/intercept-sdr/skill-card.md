## Description: <br>
Control and query a running iNTERCEPT SDR signal intelligence platform through its REST API for SDR device status, signal decoders, streams, recordings, scanner controls, remote agents, and system health. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brandongraves08](https://clawhub.ai/user/brandongraves08) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, radio operators, and security teams use this skill to have an agent call an authorized iNTERCEPT SDR instance for SDR and SIGINT operations, including starting and stopping decoders, retrieving decoded data, and checking hardware or system state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can grant broad live monitoring and process-control authority over an iNTERCEPT SDR instance. <br>
Mitigation: Install it only for an authorized instance you control, restrict the service to trusted networks, and require explicit user confirmation before scans, recordings, killall, or remote-agent actions. <br>
Risk: Default credentials or exposed session-based authentication could let unintended users control SDR functions. <br>
Mitigation: Change default credentials before use and protect session cookies and CSRF tokens as sensitive credentials. <br>
Risk: Decoded communications and location-adjacent radio data may be sensitive. <br>
Mitigation: Require explicit user approval before retrieving decoded communications and limit use to lawful, authorized monitoring. <br>


## Reference(s): <br>
- [iNTERCEPT API Reference](artifact/references/api_reference.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/brandongraves08/intercept-sdr) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with REST endpoint descriptions, curl-style shell commands, and JSON request guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use session cookies, CSRF tokens, SSE streams, and WebSocket URLs when controlling an authorized local iNTERCEPT server.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, artifact metadata, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
