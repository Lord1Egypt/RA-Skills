## Description: <br>
Efficient, secure agent-to-agent communication protocol. 40-60% token reduction, built-in privacy, Ed25519 signatures. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Swahilipapi](https://clawhub.ai/user/Swahilipapi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external agent builders use Molt Speak to document and apply a structured agent-to-agent communication protocol for handshakes, queries, responses, task delegation, tool invocation, consent handling, classification, and signed messages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The reviewed artifact documents a protocol and references an optional npm SDK, but the scanner did not review executable SDK behavior. <br>
Mitigation: Before installing or relying on the SDK, verify the package source, pin a version, and review the implementation. <br>
Risk: Protocol claims around signatures, tool use, and PII consent may not protect users unless enforced by the implementation. <br>
Mitigation: Confirm that peer authentication, signature verification, tool-use approval, and PII consent checks are enforced before production use. <br>


## Reference(s): <br>
- [MoltSpeak website](https://www.moltspeak.xyz) <br>
- [MoltSpeak documentation](https://www.moltspeak.xyz/pages/docs.html) <br>
- [MoltSpeak GitHub repository](https://github.com/Swahilipapi/MoltSpeak) <br>
- [ClawHub skill page](https://clawhub.ai/Swahilipapi/moltspeak) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON message examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only artifact; no executable behavior was present in the reviewed skill files.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
