## Description: <br>
Generates a structured Markdown summary format for OpenClaw memory flushes and conversation compaction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hanxiao-bot](https://clawhub.ai/user/hanxiao-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw agents and developers use this skill during memory flush or compaction to preserve conversation state, tool usage, user requests, pending tasks, key files, current work, timeline details, and resume instructions in MEMORY.md. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Memory summaries can persist secrets, credentials, private personal data, or sensitive business details in local MEMORY.md files. <br>
Mitigation: Review summaries before long-term retention, avoid including sensitive content, and periodically inspect MEMORY.md in shared or long-lived workspaces. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hanxiao-bot/openclaw-compact-summary) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Guidance] <br>
**Output Format:** [Structured Markdown memory summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes conversation scope, tools used, user requests, todo items, key files, current work, timeline, and resume instruction sections.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
