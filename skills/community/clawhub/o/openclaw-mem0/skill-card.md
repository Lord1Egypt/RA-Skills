## Description: <br>
Adds intelligent long-term memory to agents for auto-capturing, recalling, and managing user facts and preferences across sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xRay2016](https://clawhub.ai/user/xRay2016) <br>

### License/Terms of Use: <br>
Apache-2.0 <br>


## Use Case: <br>
Developers and agent operators use this plugin to add persistent Mem0-backed session and long-term memory to OpenClaw-compatible agents. It supports automatic memory recall and capture, manual memory tools, and basic CLI memory management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent memory can automatically store and reuse conversation-derived personal context, including through a hosted Mem0 service. <br>
Mitigation: Install only when persistent memory is desired, use a trusted Mem0 cloud or self-hosted endpoint, and periodically review or delete stored memories. <br>
Risk: Auto-capture may save sensitive details that users did not intend to persist. <br>
Mitigation: Disable auto-capture for sensitive workflows and customize extraction rules to exclude data that should not be stored. <br>
Risk: Mem0 API keys and hosted endpoint configuration protect access to memory data. <br>
Mitigation: Protect the API key, prefer environment variables or secret storage, and configure only trusted endpoints. <br>


## Reference(s): <br>
- [ClawHub Openclaw Mem0 Release Page](https://clawhub.ai/xRay2016/openclaw-mem0) <br>
- [Mem0](https://mem0.ai) <br>
- [Mem0 Open Source Project](https://github.com/mem0ai/mem0) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON configuration examples, shell command examples, and text tool responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can store, retrieve, list, search, and delete memories through Mem0 platform or self-hosted backends.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
