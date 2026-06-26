## Description: <br>
Personify Memory helps OpenClaw agents preserve user-requested and detected important moments into layered memory files, daily logs, and archives for later retrieval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lsa03](https://clawhub.ai/user/lsa03) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External OpenClaw users and agent developers use this skill to let an agent recognize memory-worthy moments, save explicit user memory requests, maintain structured personal memory files, and run scheduled backup, review, and archive routines. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads raw OpenClaw conversation logs and stores long-term personal memory artifacts. <br>
Mitigation: Review configured session and memory paths before installation, limit file permissions to the intended agent account, and avoid enabling the skill for conversations that should not be persisted. <br>
Risk: Scheduled backup, review, archive, and cleanup jobs can persist, move, or prune session history. <br>
Mitigation: Run scripts in test mode where available, back up session logs before enabling cron, and verify the configured retention and cleanup behavior matches user expectations. <br>
Risk: Optional external model validation may send memory-review content to an LLM provider. <br>
Mitigation: Disable or scope external LLM validation when sensitive logs are present, and use dedicated least-privilege API credentials such as a scoped LLM_API_KEY. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/lsa03/personify-memory) <br>
- [Publisher Profile](https://clawhub.ai/user/lsa03) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [default-config.json](artifact/config/default-config.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance with JavaScript snippets, shell commands, JSON configuration, JSONL session backups, and memory files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes and updates local memory artifacts such as MEMORY.md, knowledge-base.md, emotion-memory.json, daily JSONL backups, archive files, state files, and memory indexes.] <br>

## Skill Version(s): <br>
1.3.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
