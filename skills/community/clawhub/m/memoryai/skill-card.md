## Description: <br>
Long-term memory for AI agents that stores and recalls preferences, decisions, and context across sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ch270035](https://clawhub.ai/user/ch270035) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use MemoryAI to give an OpenClaw agent persistent memory, session bootstrap context, recall, profile lookup, and session summaries. It is suited for workflows where the agent is intentionally allowed to retain long-term user and project context through a cloud memory service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can upload local conversation excerpts and long-term memory content to a cloud service. <br>
Mitigation: Install only when cloud retention is intended, configure the endpoint deliberately, and avoid syncing transcripts or memories that should not leave the local environment. <br>
Risk: The sync and tracking flows may run repeatedly in the background and process local session transcripts. <br>
Mitigation: Confirm whether background transcript syncing should be enabled, limit or disable cron and per-message hooks when continuous syncing is not required, and review endpoint retention, deletion, and redaction policies. <br>
Risk: The skill requires a sensitive API credential. <br>
Mitigation: Provide HM_API_KEY through environment or local configuration with normal secret-handling controls, and rotate the key if it is exposed. <br>


## Reference(s): <br>
- [MemoryAI service](https://memoryai.dev) <br>
- [ClawHub MemoryAI release](https://clawhub.ai/ch270035/memoryai) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/ch270035) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with CLI command examples and plain-text command output from the memory client.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and an HM_API_KEY credential; default endpoint is https://memoryai.dev.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata, SKILL.md frontmatter, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
