## Description:

Manage, optimize, and troubleshoot OpenClaw memory, including MEMORY.md curation, daily logs, memory_search tuning, compaction survival, and vector or hybrid search configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weareallsatoshin](https://clawhub.ai/user/weareallsatoshin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to configure, maintain, search, and troubleshoot agent memory files, durable notes, compaction behavior, indexing, and memory plugins.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Durable memory may capture private chats, credentials, customer data, or sensitive notes.

Mitigation: Set explicit rules for what must never be stored and review memory files before enabling durable or automatic memory workflows.

Risk: Broad extraPaths or external indexing can expose files outside the intended OpenClaw workspace.

Mitigation: Limit extraPaths to intended Markdown sources and avoid cloud or auto-capture plugins unless their data handling is acceptable.

Risk: QMD is an optional external backend that requires a separate install.

Mitigation: Prefer pinned or sandboxed QMD installs and review the backend before using it with sensitive memory content.

## Reference(s):

- [QMD backend](https://github.com/tobi/qmd)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with configuration examples and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend edits to memory files, OpenClaw configuration, or agent operating rules.]

## Skill Version(s):

2.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
