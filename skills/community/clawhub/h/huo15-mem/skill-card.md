## Description: <br>
火一五记忆 manages personal and shared memory files by enterprise WeChat chat_id so an agent can separate user-specific and shared knowledge. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jobzhao15](https://clawhub.ai/user/jobzhao15) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and workspace administrators use this skill to classify chat-derived memories into per-user and shared Markdown files, then load the appropriate memory for each enterprise WeChat chat_id. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Chat-derived information may be written to persistent local memory, including shared memory, with unclear consent and retention controls. <br>
Mitigation: Review the skill before installing it, use it only where persistent local memory is acceptable, and prefer saving only on explicit user request. <br>
Risk: Shared memory can expose user- or project-specific information to other chats that load the same shared memory file. <br>
Mitigation: Inspect and delete saved entries regularly, and keep personal memories in per-user files while reserving shared memory for information intended for all users. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jobzhao15/huo15-mem) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown memory files with optional shell commands for inspection and cleanup] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores memories under per-user and shared local memory paths.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
