## Description: <br>
HAI Agent Framework guides agents in configuring a hook-based AI agent framework with automatic memory extraction and predefined specialist agent roles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dragons777-cpu](https://clawhub.ai/user/dragons777-cpu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to set up hook-driven agent workflows, persist conversation memory, and apply specialist roles for code review, test generation, security scanning, and documentation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic hook execution can run local scripts during session, tool, and message events. <br>
Mitigation: Review hook definitions and referenced scripts before enabling them, keep only necessary events active, and confirm how to disable hooks. <br>
Risk: Conversation-memory persistence can store user preferences, corrections, decisions, and conversation summaries locally. <br>
Mitigation: Limit what memory files may store, avoid sensitive data, and provide a clear process to inspect and delete saved memory. <br>


## Reference(s): <br>
- [Artifact SKILL.md](SKILL.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/dragons777-cpu/hai-agent-framework) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline JSON, bash, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May describe local hook scripts and memory files that should be reviewed before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and artifact SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
