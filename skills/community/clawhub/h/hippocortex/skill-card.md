## Description: <br>
Provides an OpenClaw agent with persistent long-term memory by automatically remembering and recalling conversations, facts, and preferences across sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vmaiops-alt](https://clawhub.ai/user/vmaiops-alt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add persistent Hippocortex memory to OpenClaw agents, including recall before responses and capture after memorable exchanges. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Conversation-derived data may be sent to and persisted by Hippocortex with broad automatic triggers. <br>
Mitigation: Install only when persistent memory is intended, avoid storing secrets or regulated information, and review provider controls for inspecting or deleting memories. <br>
Risk: A plaintext workspace configuration file can contain the Hippocortex API key and base URL. <br>
Mitigation: Prefer environment variables for credentials and verify the configured base URL before use. <br>


## Reference(s): <br>
- [Hippocortex Setup Guide](references/setup-guide.md) <br>
- [ClawHub release page](https://clawhub.ai/vmaiops-alt/hippocortex) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown with JSON and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Hippocortex API requests for memory synthesis, capture, and compilation; memory use should not block normal responses.] <br>

## Skill Version(s): <br>
2.2.2 (source: server release evidence; artifact _meta.json reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
