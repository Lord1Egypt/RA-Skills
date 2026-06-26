## Description: <br>
MiniMax Agent self-evolution system with 5-layer memory for continuous learning, error analysis, and persistent personalized context management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ruiyongwang](https://clawhub.ai/user/ruiyongwang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agents use this skill to add structured cross-session memory, learning logs, failure analysis, and self-improvement prompts to MiniMax Agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist conversation-derived context and user preferences across sessions. <br>
Mitigation: Require explicit user confirmation before writing memories, and provide a review, expiry, and deletion process for saved entries. <br>
Risk: Error logging can capture raw command output or sensitive context. <br>
Mitigation: Redact secrets, personal data, and unnecessary command output before saving error or learning logs. <br>
Risk: Persisted lessons may steer future behavior using stale or low-confidence information. <br>
Mitigation: Use confidence labels, keep session notes lean, and periodically review or remove obsolete memories. <br>


## Reference(s): <br>
- [Max-Self-Improvement ClawHub page](https://clawhub.ai/ruiyongwang/max-self-improvement) <br>
- [Architecture](references/architecture.md) <br>
- [Evolution Cases](references/evolution_cases.md) <br>
- [Memory Templates](references/memory_templates.md) <br>
- [Learning Templates](assets/SKILL-TEMPLATE.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with file templates and shell script prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces persistent memory entries and learning logs when adopted by an agent.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
