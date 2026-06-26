## Description: <br>
Helps agents establish, reuse, and message through labeled subagent sessions for cross-agent collaboration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[panmenglin](https://clawhub.ai/user/panmenglin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill when agents need a persistent communication channel for task coordination. It guides agents to find or create labeled subagent sessions, send messages, and avoid using human-agent conversation sessions for agent-to-agent work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create and preserve long-lived subagent communication sessions through shell-based session management without explicit expiry or cleanup limits. <br>
Mitigation: Require confirmation before spawning or protecting sessions, and document a process to list and clean up protected sessions. <br>
Risk: Messages may include private context intended for a specific agent session. <br>
Mitigation: Verify the target agent and session key before sending private or sensitive context, and restrict acceptable session labels or keys. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/panmenglin/inter-agent-communication) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code] <br>
**Output Format:** [Markdown guidance with JavaScript examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes session lookup, session creation, message sending, and session protection workflow guidance.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
