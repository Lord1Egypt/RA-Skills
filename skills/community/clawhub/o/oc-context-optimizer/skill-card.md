## Description: <br>
Optimizes OpenClaw conversation context by deduplicating and compressing messages, summarizing long chats, managing token budgets, deferring tool loading, and parallelizing tool execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[penghang1223](https://clawhub.ai/user/penghang1223) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw administrators and agent platform developers use this runtime optimizer to reduce token usage, preserve long-running conversation continuity, and load tools on demand across agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic compaction can remove or rewrite conversation context in ways that affect downstream agent decisions. <br>
Mitigation: Enable the skill only in administrator-controlled scopes and keep audit logs or diffs for compaction events. <br>
Risk: Summaries and token-budget logs can expose sensitive content, file paths, or operational details. <br>
Mitigation: Redact secrets and sensitive paths before storing summaries, preserved-file lists, or token usage history. <br>
Risk: Parallel execution, retries, and deferred tool loading can increase the impact of tools that write, send, delete, or call external services. <br>
Mitigation: Use conservative retry and parallelism settings, and restrict high-impact tools to explicitly approved administrator configurations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/penghang1223/oc-context-optimizer) <br>
- [Artifact skill documentation](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [JSON results, Markdown or text summaries, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can update conversation context, token-budget state, and tool execution ordering when enabled.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
