## Description: <br>
A memory management system powered by ReMe that provides persistent cross-session memory, automatic user preference application, and intelligent context compression for OpenClaw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[minybear](https://clawhub.ai/user/minybear) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to persist user preferences, retrieve prior context, learn from corrections, and compress long-running conversation state across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent cross-session memory may store user preferences, session summaries, or sensitive personal data longer than intended. <br>
Mitigation: Decide what must never be stored before enabling the skill, avoid saving secrets or sensitive personal data, and regularly review and purge .reme, MEMORY.md, and memory/ files. <br>
Risk: Weak consent and retention controls may allow broad session summaries or preferences to be saved without enough user review. <br>
Mitigation: Require explicit confirmation before saving broad session summaries or durable preferences, and keep timestamps so stale entries can be removed. <br>
Risk: Automatically reapplied preferences can repeat outdated or incorrect instructions across future sessions. <br>
Mitigation: Review retrieved memories before applying them, filter by relevance and recency, and update or delete obsolete preferences. <br>
Risk: Stored file-handling preferences may cause generated files to be sent automatically when that is not desired. <br>
Mitigation: Require explicit confirmation before auto-sending generated files and disable or narrow auto-send rules when handling private or sensitive outputs. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/minybear/memory-reme) <br>
- [SKILL.md](SKILL.md) <br>
- [Memory File Structure Guide](references/memory-structure.md) <br>
- [Best Practices for Memory Management](references/best-practices.md) <br>
- [Common User Preferences Reference](references/common-prefs.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local memory files such as MEMORY.md, memory/YYYY-MM-DD.md, and .reme data when its scripts are used.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata and README) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
