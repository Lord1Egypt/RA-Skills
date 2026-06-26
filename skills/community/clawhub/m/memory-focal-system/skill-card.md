## Description: <br>
Memory Focal System manages persistent local memory for agents by classifying messages, loading relevant memory, writing new memories, tagging content, and applying forgetting-curve cleanup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zcz-user](https://clawhub.ai/user/zcz-user) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external ClawHub users use this skill to add local persistent memory workflows to an agent, including message classification, selective memory loading, memory search, tagging, and cleanup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist conversation-derived content in local memory files. <br>
Mitigation: Use it only when persistent memory is intended, avoid storing secrets or confidential content, and regularly inspect and delete generated memory files. <br>
Risk: Automatic memory writing may store more user context than expected. <br>
Mitigation: Disable automatic writing unless users have opted in and review the memory configuration before deployment. <br>
Risk: Optional LLM auto-tagging may send memory text to external model APIs. <br>
Mitigation: Disable external auto-tagging unless API use and data handling are approved for the deployment environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zcz-user/memory-focal-system) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with Python snippets, shell commands, and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces memory context objects and local JSONL memory records when used at runtime] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
