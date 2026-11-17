## Description:

Optimize conversation context by deduplicating and compressing messages, summarizing long chats, tracking token budgets, parallelizing tool calls, and loading tool descriptions on demand.

This skill is ready for commercial/non-commercial use.

## Publisher:

[penghang1223](https://clawhub.ai/user/penghang1223)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw administrators use this skill to reduce context size, manage token budgets, and make tool execution more efficient across agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic context rewriting can omit, compress, or reshape information that agents later rely on.

Mitigation: Review compaction behavior on representative conversations and disable or narrow automatic compaction for workflows that require exact context retention.

Risk: Deferred tool loading changes which tool descriptions agents see and may expose or hide capabilities unexpectedly.

Mitigation: Review the always-loaded tools, deferred categories, keywords, and trigger weights before enabling the skill in sensitive environments.

Risk: Private files, chat content, OAuth-related data, or business data may pass through summaries, logs, or runtime state.

Mitigation: Confirm secret redaction, logging paths, and retention behavior before using the skill with private or regulated data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/penghang1223/skills/oc-context-optimizer)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, shell command examples, Python integration snippets, and JSON status or configuration data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce compressed conversation summaries, token budget reports, deferred-tool search results, and parallel tool execution results.]

## Skill Version(s):

1.2.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
