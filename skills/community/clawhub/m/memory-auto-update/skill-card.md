## Description: <br>
Memory Auto Update helps an agent identify important conversation content, summarize it for user confirmation, and save structured memory entries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhuqingsonga](https://clawhub.ai/user/zhuqingsonga) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to capture decisions, to-dos, facts, preferences, appointments, and project updates from the current conversation into reviewable memory notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Conversation content may be persisted across sessions through broad memory trigger phrases. <br>
Mitigation: Use the skill only when persistent conversation-derived memory is desired, and require preview and confirmation before saving important entries. <br>
Risk: Retention and file-write scope are not clearly bounded by the release evidence. <br>
Mitigation: Confirm the memory storage path, review and deletion process, and whether automatic writes can be disabled before deployment. <br>
Risk: Extracted memories can be incomplete or inaccurate. <br>
Mitigation: Have users review generated summaries and edit, delete, or supplement entries before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhuqingsonga/memory-auto-update) <br>
- [README](artifact/README.md) <br>
- [Usage tips](artifact/tips.md) <br>
- [Skill metadata homepage](https://github.com/zhuqingsonga/memory-auto-update) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown memory entries and concise confirmation text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write date-based local memory files after user review or configured triggers] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
