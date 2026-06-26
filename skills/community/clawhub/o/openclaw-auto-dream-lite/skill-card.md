## Description: <br>
Lightweight memory consolidation for OpenClaw agents that turns scattered daily logs into structured long-term memory through daily dream cycles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[myclaw-ai](https://clawhub.ai/user/myclaw-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and operators use this skill to consolidate recent daily logs into MEMORY.md, maintain a dream log, and surface concise memory updates or stale threads. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can schedule recurring local edits to MEMORY.md and files under memory/. <br>
Mitigation: Use it only in workspaces where automatic memory updates are acceptable, and review memory files for sensitive content before enabling the cron job. <br>
Risk: Memory consolidation may accidentally produce an incorrect or undesirable MEMORY.md update. <br>
Mitigation: Keep the documented pre-dream backup, preserve daily logs, and restore MEMORY.md.pre-dream if a dream cycle corrupts or substantially changes memory. <br>
Risk: Recurring consolidation can expose personal or project details from daily logs in summary notifications or dream-log entries. <br>
Mitigation: Limit use to trusted workspaces and review MEMORY.md, memory daily logs, and dream-log output for sensitive content. <br>


## Reference(s): <br>
- [Auto-Dream execution prompt](references/dream-prompt.md) <br>
- [Memory template](references/memory-template.md) <br>
- [ClawHub skill page](https://clawhub.ai/myclaw-ai/openclaw-auto-dream-lite) <br>
- [MyClaw.ai](https://myclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and cron configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces concise user notifications, appends dream-log entries, updates MEMORY.md, and marks daily logs as consolidated.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
