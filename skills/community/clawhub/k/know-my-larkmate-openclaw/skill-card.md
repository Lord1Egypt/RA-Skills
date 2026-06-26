## Description: <br>
Sync recent Lark context into OpenClaw daily notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lobster-de-luo](https://clawhub.ai/user/lobster-de-luo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and developers use this skill to read recent Lark activity, identify current work context, and append concise, source-linked updates to daily notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read broad Lark workplace activity and persist summaries into OpenClaw daily notes. <br>
Mitigation: Enable it only for intended Lark context sync, keep scopes read-only and as narrow as possible, and periodically review or delete generated daily notes. <br>
Risk: Scheduled heartbeat runs may import recent workplace context without an immediate user prompt. <br>
Mitigation: Confirm the heartbeat cadence and behavior before enabling scheduled runs, and avoid offline access unless background sync is required. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/lobster-de-luo/know-my-larkmate-openclaw) <br>
- [Install Checklist](references/install-spec.md) <br>
- [Recent Context Guide](references/recent-context-guide.md) <br>
- [Heartbeat Template](assets/HEARTBEAT.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Configuration] <br>
**Output Format:** [Markdown daily-note entries with supporting shell commands and setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Updates are intended for memory/YYYY-MM-DD.md and should remain factual, recent, and source-linked.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
