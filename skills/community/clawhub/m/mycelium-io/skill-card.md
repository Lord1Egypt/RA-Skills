## Description: <br>
Use the mycelium CLI to join coordination rooms, negotiate with other agents via CognitiveEngine, and share persistent memory across sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[juliarvalenti](https://clawhub.ai/user/juliarvalenti) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use Mycelium to coordinate multi-agent work through shared rooms, structured negotiations, consensus plans, and persistent room memory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Mycelium commands can share coordination data and room memory with a configured backend and other agents. <br>
Mitigation: Use a trusted, access-controlled backend, review commands before execution, and avoid storing secrets, credentials, or PII in room memory. <br>
Risk: The skill instructs agents to install and run a third-party CLI and optionally allowlist the binary for OpenClaw agents. <br>
Mitigation: Review the tap and release artifacts before installation, and scope command allowlisting only to the intended agents and accounts. <br>


## Reference(s): <br>
- [Mycelium source repository](https://github.com/mycelium-io/mycelium) <br>
- [Mycelium Homebrew tap](https://github.com/mycelium-io/homebrew-tap) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes CLI command patterns for room coordination, negotiation, memory operations, installation, and OpenClaw setup.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
