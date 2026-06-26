## Description: <br>
Inter-agent communication via shared JSON file for OpenClaw instances that need to exchange messages, coordinate, or pass information across local, SSH, or shared-storage environments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sonerbo](https://clawhub.ai/user/sonerbo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to coordinate two or more OpenClaw or Kiro agents through a shared JSON message queue. It supports sending, reading, and deleting agent messages with simple command-line scripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Messages are stored in a shared file that may persist sensitive or untrusted content. <br>
Mitigation: Use a dedicated queue file with restrictive permissions and avoid placing secrets or authoritative instructions in chat messages. <br>
Risk: Received messages may contain incorrect, unsafe, or misleading instructions for another agent. <br>
Mitigation: Treat received messages as untrusted input and review them before acting on their contents. <br>
Risk: Deleting message IDs can remove queue history that has not been fully processed. <br>
Mitigation: Delete only message IDs that have been processed and are no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sonerbo/kiro-agent-chat) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text command output and JSON queue entries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Messages are persisted in a user-managed shared JSON file and filtered by receiver name or broadcast.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
