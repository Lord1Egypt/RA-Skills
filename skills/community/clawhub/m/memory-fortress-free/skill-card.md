## Description: <br>
AI Agent six-layer memory system that helps preserve context, decisions, and lessons with a write-ahead logging workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and other agent users use this skill to set up persistent local memory files and workflows for long-running projects, decision tracking, and cross-session context recovery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks an agent to retain conversation details persistently, which can capture personal, business, or sensitive information without clear consent. <br>
Mitigation: Require the agent to ask before storing personal, business, or sensitive details, and inspect generated memory files regularly. <br>
Risk: The skill combines local memory with optional cloud backup, Mem0, vector, or provider-backed features. <br>
Mitigation: Keep cloud backup, Mem0, vector, and provider features disabled unless they are explicitly configured and approved. <br>
Risk: Maintenance guidance includes recursive deletion of local memory data. <br>
Mitigation: Avoid destructive cleanup commands unless a backup exists and the operator understands the stored memory will be erased. <br>


## Reference(s): <br>
- [Detailed Reference](artifact/references/detail.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/thcjp/skills/memory-fortress-free) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces instructions for memory files, local command usage, and optional provider configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
