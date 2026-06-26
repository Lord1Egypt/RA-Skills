## Description: <br>
Guides agents in using OpenClaw's multi-layered memory format with long-term, daily, and session memory records. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hanxiao-bot](https://clawhub.ai/user/hanxiao-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to structure local OpenClaw memory files so important decisions, summaries, follow-up items, and technical notes remain searchable across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent memory files may retain secrets, credentials, or sensitive personal data if users store them there. <br>
Mitigation: Avoid writing sensitive data to MEMORY.md or daily memory files, and periodically review or delete memory files in private workspaces. <br>
Risk: Daily memory records can become excessive or stale if they are never cleaned up. <br>
Mitigation: Distill durable information into MEMORY.md and periodically remove or archive daily entries that are no longer useful. <br>


## Reference(s): <br>
- [OpenClaw Memory Format on ClawHub](https://clawhub.ai/hanxiao-bot/openclaw-memory-format) <br>
- [hanxiao-bot publisher profile](https://clawhub.ai/user/hanxiao-bot) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown guidance with structured file path and section examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Describes MEMORY.md, daily memory files, session memory, search usage, flush triggers, and cleanup practices.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
