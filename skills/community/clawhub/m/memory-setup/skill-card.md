## Description: <br>
Enable and configure Moltbot/Clawdbot memory search for persistent context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jrbobbyhansen-pixel](https://clawhub.ai/user/jrbobbyhansen-pixel) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to configure persistent memory search, create a MEMORY.md structure, set daily memory logs, and troubleshoot memory recall for Moltbot or Clawdbot. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Memory and session indexing can make sensitive past context easier to retrieve, including passwords, tokens, private business information, or regulated personal data if users place it in memory files or logs. <br>
Mitigation: Decide what sources to index before enabling memory search, avoid storing sensitive data in MEMORY.md or memory logs, and use a local provider or review hosted embedding-provider policies for private environments. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jrbobbyhansen-pixel/memory-setup) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance, shell commands] <br>
**Output Format:** [Markdown with JSON configuration examples and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides memorySearch configuration, MEMORY.md and memory directory templates, AGENTS.md guidance, and troubleshooting steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
