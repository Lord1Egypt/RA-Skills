## Description: <br>
Optimize OpenClaw token usage and cost by auditing context injection, trimming workspace files (AGENTS.md/SOUL.md/MEMORY.md and daily memory), enabling prompt caching, heartbeat, context pruning, compaction, memory search or qmd, subagents, model tiering, and cron frequency. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ccjingeth](https://clawhub.ai/user/ccjingeth) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to audit OpenClaw token usage, reduce avoidable context and model calls, and plan config changes for lower token spend while preserving answer quality. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Suggested config and memory changes could alter agent behavior or expose sensitive context if applied without review. <br>
Mitigation: Back up openclaw.json and memory files, verify provider support, and restrict memory-search or qmd paths to non-sensitive content before applying changes. <br>
Risk: Heartbeat and subagent settings may create ongoing or parallel model calls. <br>
Mitigation: Enable heartbeat or subagents only when the user explicitly wants those calls, and use low-cost models and quiet windows where appropriate. <br>


## Reference(s): <br>
- [OpenClaw token optimization reference](references/openclaw-token-optimization.md) <br>
- [ClawHub skill page](https://clawhub.ai/ccjingeth/openclaw-token-save) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, code, guidance] <br>
**Output Format:** [Markdown with JSON configuration snippets and rollout guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include approximate token estimates, file size targets, and suggested OpenClaw config edits for human review.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
