## Description: <br>
Memory Archiver adds OpenClaw memory search, extraction, session notes, and consolidation across daily, weekly, and long-term workspace memory files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[amd5](https://clawhub.ai/user/amd5) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to persist useful conversation context, search prior memory during new messages, maintain session notes, and consolidate memory into longer-term records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically capture, persist, and replay user conversation content as long-term memory. <br>
Mitigation: Install only in workspaces where persistent memory is wanted; avoid credentials, private personal data, and confidential project details unless they are acceptable to store and recall later. <br>
Risk: The skill installs hooks and scheduled jobs that run automatically with limited user control. <br>
Mitigation: Review hook and cron registrations after installation, confirm where memory is stored, and disable the memory hook when automatic capture or recall is not desired. <br>
Risk: Stored memory may later be injected into prompts even when it is stale or no longer appropriate. <br>
Mitigation: Periodically inspect, prune, or delete stored memory files and indexes before using the skill with sensitive or changing work contexts. <br>


## Reference(s): <br>
- [Memory Archiver on ClawHub](https://clawhub.ai/amd5/memory-archiver) <br>
- [Publisher profile: amd5](https://clawhub.ai/user/amd5) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown memory files, prompt-injected text, and command/configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates local OpenClaw workspace memory files, hook registration, cron jobs, and memory indexes.] <br>

## Skill Version(s): <br>
10.3.0 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
