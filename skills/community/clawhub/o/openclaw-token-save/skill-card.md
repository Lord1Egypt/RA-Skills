## Description:

Optimize OpenClaw token usage and cost by auditing context injection, trimming workspace files (AGENTS.md/SOUL.md/MEMORY.md and daily memory), enabling prompt caching, heartbeat, context pruning, compaction, memory search or qmd, subagents, model tiering, and cron frequency.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ccjingeth](https://clawhub.ai/user/ccjingeth)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to audit OpenClaw token costs, reduce injected context, tune caching and pruning behavior, and produce concrete OpenClaw configuration guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory writes and broad local memory indexing can retain sensitive data if enabled on inappropriate paths or workloads.

Mitigation: Review suggested OpenClaw config changes before applying them, scope memoryFlush, memorySearch, and qmd indexing to understood paths, and avoid persisting secrets, credentials, private logs, or broad workspaces without a retention and deletion plan.

Risk: Prompt caching and memory search settings may be unsupported by some providers, models, or OpenClaw versions.

Mitigation: Confirm provider, model, and OpenClaw version support before applying config keys, and treat token counts or savings estimates as approximate unless measured directly.

## Reference(s):

- [OpenClaw token optimization reference](artifact/references/openclaw-token-optimization.md)
- [OpenClaw Token Optimizer ClawHub page](https://clawhub.ai/ccjingeth/skills/openclaw-token-save)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance, code, shell commands]

**Output Format:** [Markdown with JSON snippets and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include audit summaries, estimated savings, config patches, file-trimming targets, and rollout plans.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
