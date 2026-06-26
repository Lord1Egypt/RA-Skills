## Description: <br>
Install, configure, diagnose, and operate the openclaw-mem0 long-term memory plugin for OpenClaw agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nyrosveil](https://clawhub.ai/user/nyrosveil) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to install, configure, and troubleshoot long-term memory for OpenClaw agents in Mem0 platform mode or local open-source mode. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The memory plugin can retain and reuse long-term user information across agent sessions. <br>
Mitigation: Install it only when persistent memory is desired, avoid storing secrets, and periodically inspect or delete stored memories. <br>
Risk: Automatic recall or capture may be broader than intended for sensitive workflows. <br>
Mitigation: Disable autoCapture or autoRecall when opt-in memory behavior is required. <br>
Risk: Platform mode requires a Mem0 API key. <br>
Mitigation: Keep the API key in an environment variable rather than hard-coding it in configuration files. <br>
Risk: Open-source mode depends on local Ollama, Qdrant, and a writable absolute history database path. <br>
Mitigation: Verify local services are running and set historyDbPath to an absolute writable path before relying on memory storage. <br>


## Reference(s): <br>
- [openclaw-mem0 Troubleshooting](references/troubleshooting.md) <br>
- [Mem0](https://mem0.ai) <br>
- [Mem0 Platform](https://app.mem0.ai) <br>
- [ClawHub Skill Page](https://clawhub.ai/nyrosveil/mem0-config) <br>
- [Publisher Profile](https://clawhub.ai/user/nyrosveil) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup, diagnostics, and troubleshooting guidance for Mem0-backed OpenClaw memory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
