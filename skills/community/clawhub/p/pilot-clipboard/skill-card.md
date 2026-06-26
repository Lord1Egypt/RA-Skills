## Description: <br>
Shared clipboard for quick text and data snippets between agents over Pilot Protocol. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
AGPL-3.0 <br>


## Use Case: <br>
Developers and agent operators use this skill to exchange short text snippets, command output, and small data payloads between agents over Pilot Protocol without transferring files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Clipboard content sent over Pilot Protocol can include secrets, tokens, private paths, host details, or sensitive command output. <br>
Mitigation: Review and redact copied content before sending it, and send only to destination agents you know and trust. <br>
Risk: Received clipboard messages may contain untrusted or unsafe text, including commands or data that should not be run blindly. <br>
Mitigation: Inspect received content before executing it, storing it, or relying on it in downstream work. <br>
Risk: The workflow depends on a local Pilot Protocol setup, the pilotctl binary, jq, and a running daemon. <br>
Mitigation: Confirm those dependencies and the intended destination agent before using copy or paste commands. <br>


## Reference(s): <br>
- [Pilot Protocol homepage](https://pilotprotocol.network) <br>
- [ClawHub skill listing](https://clawhub.ai/teoslayer/pilot-clipboard) <br>
- [Publisher profile](https://clawhub.ai/user/teoslayer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash and JSON snippets for Pilot Protocol clipboard workflows.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces user-directed clipboard command patterns and small text or JSON message payload examples; requires pilotctl and jq.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence; artifact frontmatter lists 1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
