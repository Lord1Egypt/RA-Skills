## Description: <br>
Hermes Communication Bridge lets WorkBuddy and Hermes exchange messages through a shared local JSON file queue. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liuboacean](https://clawhub.ai/user/liuboacean) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to send, receive, inspect, and process asynchronous messages between WorkBuddy and Hermes through a local file queue. It supports queue-based coordination without an external service dependency. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bridge stores messages in a plaintext local queue that may be readable by trusted agents or local processes with filesystem access. <br>
Mitigation: Avoid sending secrets or sensitive data through the queue and restrict access to the shared communication directory. <br>
Risk: Queue messages can include command-like message types that may influence downstream Hermes-side handling. <br>
Mitigation: Review and constrain any Hermes-side consumer before allowing command-like messages or automated processing. <br>
Risk: Cron or auto-polling can create ongoing background processing of queued messages. <br>
Mitigation: Enable scheduled polling only when persistent background message handling is intended and monitored. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liuboacean/hermes-communication-bridge) <br>
- [README](artifact/temp-repo2/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell commands, JSON message examples, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local queue and history JSON files under the Hermes shared communication directory.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
